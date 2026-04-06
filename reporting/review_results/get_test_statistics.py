"""
This script retrieves test results from DynamoDB for the last X days
and outputs a pass/fail summary grouped by test name.

The script can be executed using the following command:
    python reporting/get_test_statistics.py

The following arguments are supported:
    --days <int>         = Number of days to look back (default: 7)
    --endpoint-url <url> = Override DynamoDB endpoint URL. Use for
                           local testing e.g. http://localhost:8000
    --sort-by <field>    = Sort output by: name, total, passes, fails,
                           pass_rate, duration (default: name)
    --output-csv <path>  = Write results to a CSV file at the given
                           path in addition to stdout output
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import boto3
from boto3.dynamodb.conditions import Attr


TABLE_NAME = "playwright-test-results"
DEFAULT_REGION = "eu-west-2"
SORT_FIELDS = ("name", "total", "passes", "fails", "pass_rate",
               "avg_duration")


def fetch_results(
    days: int,
    endpoint_url: str | None = None,
) -> list[dict[str, Any]]:
    """
    Scan the DynamoDB table for all test results within the last
    X days.

    Args:
        days (int): Number of days to look back.
        endpoint_url (str | None): Optional DynamoDB endpoint override.

    Returns:
        list[dict]: All matching test result items.
    """
    region = os.environ.get("AWS_REGION", DEFAULT_REGION)
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=region,
        endpoint_url=endpoint_url
    )
    table = dynamodb.Table(TABLE_NAME)

    since = (
        datetime.now(timezone.utc) - timedelta(days=days)
    ).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    items: list[dict[str, Any]] = []
    scan_kwargs: dict[str, Any] = {
        "FilterExpression": Attr("timestamp").gte(since)
    }

    # DynamoDB paginates at 1MB — loop until all pages retrieved
    while True:
        response = table.scan(**scan_kwargs)
        items.extend(response.get("Items", []))
        last_key = response.get("LastEvaluatedKey")
        if not last_key:
            break
        scan_kwargs["ExclusiveStartKey"] = last_key

    return items


def build_statistics(
    items: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Aggregate raw DynamoDB items into per-test statistics.

    Args:
        items (list[dict]): Raw test result items from DynamoDB.

    Returns:
        list[dict]: One summary dict per unique test name.
    """
    stats: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "total": 0,
        "passes": 0,
        "fails": 0,
        "total_duration": Decimal("0"),
    })

    for item in items:
        name = item.get("test_name", "unknown")
        outcome = item.get("outcome", "unknown")
        duration = item.get("total_duration", Decimal("0"))

        stats[name]["total"] += 1
        stats[name]["total_duration"] += Decimal(str(duration))

        if outcome == "passed":
            stats[name]["passes"] += 1
        else:
            stats[name]["fails"] += 1

    results = []
    for test_name, data in stats.items():
        total = data["total"]
        passes = data["passes"]
        pass_rate = (passes / total * 100) if total > 0 else 0.0
        avg_duration = (
            data["total_duration"] / total if total > 0
            else Decimal("0")
        )
        results.append({
            "name": test_name,
            "total": total,
            "passes": passes,
            "fails": data["fails"],
            "pass_rate": round(pass_rate, 1),
            "avg_duration": float(
                avg_duration.quantize(Decimal("0.001"))
            ),
            "total_duration": float(
                data["total_duration"].quantize(Decimal("0.001"))
            ),
        })

    return results


def sort_results(
    results: list[dict[str, Any]],
    sort_by: str,
) -> list[dict[str, Any]]:
    """
    Sort the statistics list by the given field.

    Args:
        results (list[dict]): The statistics to sort.
        sort_by (str): The field name to sort by.

    Returns:
        list[dict]: Sorted statistics.
    """
    reverse = sort_by != "name"
    return sorted(results, key=lambda r: r[sort_by], reverse=reverse)


def print_summary(
    results: list[dict[str, Any]],
    days: int,
) -> None:
    """
    Print the statistics as a formatted table to stdout.

    Args:
        results (list[dict]): The sorted statistics to display.
        days (int): The number of days the results cover.
    """
    if not results:
        print(f"No test results found in the last {days} day(s).")
        return

    # Calculate column widths dynamically based on content
    name_w = max(len(r["name"]) for r in results)
    name_w = max(name_w, len("Test Name"))

    header = (
        f"{'Test Name':<{name_w}}  "
        f"{'Total':>7}  "
        f"{'Passes':>7}  "
        f"{'Fails':>6}  "
        f"{'Pass Rate':>10}  "
        f"{'Avg Time (s)':>12}"
    )
    divider = "-" * len(header)

    print(f"\nTest Statistics — last {days} day(s)\n")
    print(header)
    print(divider)

    for r in results:
        print(
            f"{r['name']:<{name_w}}  "
            f"{r['total']:>7}  "
            f"{r['passes']:>7}  "
            f"{r['fails']:>6}  "
            f"{r['pass_rate']:>9.1f}%  "
            f"{r['avg_duration']:>12.3f}"
        )

    print(divider)

    # Totals row
    total_runs = sum(r["total"] for r in results)
    total_passes = sum(r["passes"] for r in results)
    total_fails = sum(r["fails"] for r in results)
    overall_rate = (
        round(total_passes / total_runs * 100, 1)
        if total_runs > 0 else 0.0
    )
    overall_avg = (
        sum(r["total_duration"] for r in results) / total_runs
        if total_runs > 0 else 0.0
    )

    print(
        f"{'TOTAL':<{name_w}}  "
        f"{total_runs:>7}  "
        f"{total_passes:>7}  "
        f"{total_fails:>6}  "
        f"{overall_rate:>9.1f}%  "
        f"{overall_avg:>12.3f}"
    )


CSV_HEADERS = [
    "test_name",
    "total",
    "passes",
    "fails",
    "pass_rate",
    "avg_duration_s",
]


def write_csv(
    results: list[dict[str, Any]],
    output_path: str,
) -> None:
    """
    Write the statistics to a CSV file.

    Args:
        results (list[dict]): The sorted statistics to write.
        output_path (str): The file path to write the CSV to.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "test_name": r["name"],
                "total": r["total"],
                "passes": r["passes"],
                "fails": r["fails"],
                "pass_rate": r["pass_rate"],
                "avg_duration_s": r["avg_duration"],
            })

    print(f"\nCSV written to {output_path}")


def main() -> None:
    """
    Main entry point. Parses arguments and outputs the summary.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Retrieve test statistics from DynamoDB for the "
            "last X days"
        )
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to look back (default: 7)"
    )
    parser.add_argument(
        "--endpoint-url",
        type=str,
        default=None,
        help=(
            "Override the DynamoDB endpoint URL. Use for local "
            "testing e.g. http://localhost:8000"
        )
    )
    parser.add_argument(
        "--sort-by",
        type=str,
        default="name",
        choices=SORT_FIELDS,
        help=(
            "Sort output by: name, total, passes, fails, "
            "pass_rate, avg_duration (default: name)"
        )
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default=None,
        help="Write results to a CSV file at the given path"
    )

    args = parser.parse_args()

    try:
        items = fetch_results(
            days=args.days,
            endpoint_url=args.endpoint_url,
        )
    except Exception as e:
        print(f"Error fetching results from DynamoDB: {e}")
        sys.exit(1)

    results = build_statistics(items)
    results = sort_results(results, args.sort_by)
    print_summary(results, args.days)

    if args.output_csv:
        write_csv(results, args.output_csv)


if __name__ == "__main__":
    main()
