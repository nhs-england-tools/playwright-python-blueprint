"""
This script retrieves failed test results from DynamoDB for the last
X days, groups them by test name and crash message, and outputs a
summary to help identify consistently failing tests.

The script can be executed using the following command:
    python reporting/review_results/get_failure_reasons.py

The following arguments are supported:
    --days <int>         = Number of days to look back (default: 7)
    --endpoint-url <url> = Override DynamoDB endpoint URL. Use for
                           local testing e.g. http://localhost:8000
    --sort-by <field>    = Sort output by: test_name, crash_message,
                           count (default: count)
    --output-csv <path>  = Write results to a CSV file at the given
                           path in addition to stdout output
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import boto3
from boto3.dynamodb.conditions import Attr


TABLE_NAME = "playwright-test-results"
DEFAULT_REGION = "eu-west-2"
SORT_FIELDS = ("test_name", "crash_message", "count")
NO_CRASH_MESSAGE = "(no crash message)"

CSV_HEADERS = ["test_name", "crash_message", "count", "traceback"]


def fetch_failures(
    days: int,
    endpoint_url: str | None = None,
) -> list[dict[str, Any]]:
    """
    Scan the DynamoDB table for all failed test results within the
    last X days, retrieving only the attributes needed for this report.

    Args:
        days (int): Number of days to look back.
        endpoint_url (str | None): Optional DynamoDB endpoint override.

    Returns:
        list[dict]: All matching failed test result items.
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
        "FilterExpression": (
            Attr("timestamp").gte(since) &
            Attr("outcome").eq("failed")
        ),
        "ProjectionExpression": (
            "test_name, crash_message, traceback"
        ),
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


def build_failure_groups(
    items: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Group failed test results by (test_name, crash_message) and count
    occurrences of each combination.

    Args:
        items (list[dict]): Raw failed test result items from DynamoDB.

    Returns:
        list[dict]: One summary dict per unique test/crash combination.
    """
    groups: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "traceback": ""}
    )

    for item in items:
        test_name = item.get("test_name", "unknown")
        crash_message = item.get("crash_message", NO_CRASH_MESSAGE)
        key = (test_name, crash_message)
        groups[key]["count"] += 1
        # Keep the most recent traceback seen for this group
        if item.get("traceback"):
            groups[key]["traceback"] = item["traceback"]

    return [
        {
            "test_name": test_name,
            "crash_message": crash_message,
            "count": data["count"],
            "traceback": data["traceback"],
        }
        for (test_name, crash_message), data in groups.items()
    ]


def sort_results(
    results: list[dict[str, Any]],
    sort_by: str,
) -> list[dict[str, Any]]:
    """
    Sort the failure groups by the given field.

    Args:
        results (list[dict]): The failure groups to sort.
        sort_by (str): The field name to sort by.

    Returns:
        list[dict]: Sorted failure groups.
    """
    reverse = sort_by == "count"
    return sorted(results, key=lambda r: r[sort_by], reverse=reverse)


def print_summary(
    results: list[dict[str, Any]],
    days: int,
) -> None:
    """
    Print the failure groups as a formatted table to stdout.

    Args:
        results (list[dict]): The sorted failure groups to display.
        days (int): The number of days the results cover.
    """
    if not results:
        print(f"No failures found in the last {days} day(s).")
        return

    # Calculate column widths dynamically based on content
    name_w = max(len(r["test_name"]) for r in results)
    name_w = max(name_w, len("Test Name"))

    msg_w = max(len(r["crash_message"]) for r in results)
    msg_w = max(msg_w, len("Crash Message"))

    header = (
        f"{'Test Name':<{name_w}}  "
        f"{'Crash Message':<{msg_w}}  "
        f"{'Count':>5}"
    )
    divider = "-" * len(header)

    print(f"\nFailure Reasons — last {days} day(s)\n")
    print(header)
    print(divider)

    for r in results:
        print(
            f"{r['test_name']:<{name_w}}  "
            f"{r['crash_message']:<{msg_w}}  "
            f"{r['count']:>5}"
        )

    print(divider)
    total_failures = sum(r["count"] for r in results)
    print(
        f"{'TOTAL':<{name_w}}  "
        f"{'':<{msg_w}}  "
        f"{total_failures:>5}"
    )


def write_csv(
    results: list[dict[str, Any]],
    output_path: str,
) -> None:
    """
    Write the failure groups to a CSV file.

    Args:
        results (list[dict]): The sorted failure groups to write.
        output_path (str): The file path to write the CSV to.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=CSV_HEADERS,
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()
        for r in results:
            writer.writerow({
                "test_name": r["test_name"],
                "crash_message": r["crash_message"],
                "count": r["count"],
                "traceback": r["traceback"],
            })

    print(f"\nCSV written to {output_path}")


def main() -> None:
    """
    Main entry point. Parses arguments and outputs the summary.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Retrieve failure reasons from DynamoDB for the "
            "last X days, grouped by test name and crash message"
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
        default="count",
        choices=SORT_FIELDS,
        help=(
            "Sort output by: test_name, crash_message, count "
            "(default: count)"
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
        items = fetch_failures(
            days=args.days,
            endpoint_url=args.endpoint_url,
        )
    except Exception as e:
        print(f"Error fetching results from DynamoDB: {e}")
        sys.exit(1)

    results = build_failure_groups(items)
    results = sort_results(results, args.sort_by)
    print_summary(results, args.days)

    if args.output_csv:
        write_csv(results, args.output_csv)


if __name__ == "__main__":
    main()
