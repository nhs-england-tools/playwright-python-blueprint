"""
This script uploads individual test result JSON files from the
json-output directory to a DynamoDB table called
playwright-test-results.

The DynamoDB table uses the following key structure:
    Partition Key (test_id): TEST#<test_name>
    Sort Key (timestamp): ISO 8601 timestamp (e.g. 2026-04-04T14:30:00.000Z)

AWS credentials must be configured before running this script, either
via environment variables, AWS credentials file, or IAM role (when
running on AWS infrastructure).

The following environment variables are used if present:
    - AWS_REGION: The AWS region for DynamoDB (default: eu-west-2)
    - GITHUB_RUN_ID: GitHub Actions build ID
    - GITHUB_REF_NAME: GitHub Actions branch name

The script can be executed using the following command:
    python reporting/upload_test_results.py

The following arguments are supported:
    --input-dir <path>  = Directory containing individual test JSON
                          files. Defaults to test-results/json-output
    --build-id <id>     = Build ID to associate with the results.
                          Defaults to GITHUB_RUN_ID env var or "local"
    --branch <name>     = Branch name to associate with the results.
                          Defaults to GITHUB_REF_NAME env var or "local"
    --timestamp <ts>    = ISO 8601 timestamp to use for the sort key.
                          Defaults to current UTC time
    --dry-run           = Print items without uploading to DynamoDB
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import boto3


TABLE_NAME = "playwright-test-results"
DEFAULT_REGION = "eu-west-2"


def extract_test_name(nodeid: str) -> str:
    """
    Extract the base test name from a pytest nodeid, stripping
    the file path and any parameterisation (e.g. [chromium]).

    Args:
        nodeid (str): The pytest nodeid string.

    Returns:
        str: The test name without file path or parameters.
    """
    parts = nodeid.split("::")
    test_name = parts[1] if len(parts) > 1 else nodeid
    if "[" in test_name:
        test_name = test_name[:test_name.index("[")]
    return test_name


def extract_test_file(nodeid: str) -> str:
    """
    Extract the test file stem from a pytest nodeid.

    Args:
        nodeid (str): The pytest nodeid string.

    Returns:
        str: The test filename without path or extension.
    """
    parts = nodeid.split("::")
    return Path(parts[0]).stem if parts else "unknown"


def extract_browser(nodeid: str) -> str:
    """
    Extract the browser name from a pytest nodeid if present.

    Args:
        nodeid (str): The pytest nodeid string.

    Returns:
        str: The browser name, or "unknown" if not present.
    """
    if "[" in nodeid and "]" in nodeid:
        return nodeid[nodeid.index("[") + 1:nodeid.index("]")]
    return "unknown"


def extract_crash_info(
    test_data: dict[str, Any]
) -> dict[str, Any]:
    """
    Extract crash and traceback information from a test result,
    prioritising the call phase over setup and teardown.

    Args:
        test_data (dict): The full test result dictionary.

    Returns:
        dict: A flat dictionary of sparse crash attributes, or an
              empty dict if no crash information is present.
    """
    crash_attrs: dict[str, Any] = {}

    # Check phases in priority order: call first, then setup, teardown
    for phase in ("call", "setup", "teardown"):
        phase_data = test_data.get(phase, {})

        if "crash" in phase_data and "crash_path" not in crash_attrs:
            crash = phase_data["crash"]
            crash_attrs["crash_path"] = crash.get("path", "")
            crash_attrs["crash_lineno"] = crash.get("lineno")
            crash_attrs["crash_message"] = crash.get("message", "")
            crash_attrs["crash_phase"] = phase

        if "traceback" in phase_data and "traceback" not in crash_attrs:
            crash_attrs["traceback"] = json.dumps(
                phase_data["traceback"]
            )

        if "longrepr" in phase_data and "longrepr" not in crash_attrs:
            crash_attrs["longrepr"] = phase_data["longrepr"]

        # Once call phase is processed, stop if we found crash info
        if phase == "call" and crash_attrs:
            break

    return crash_attrs


def to_decimal(value: float) -> Decimal:
    """
    Convert a float to a Decimal for DynamoDB compatibility.

    Args:
        value (float): The float value to convert.

    Returns:
        Decimal: The converted value.
    """
    return Decimal(str(round(value, 6)))


def build_dynamo_item(
    test_data: dict[str, Any],
    build_id: str,
    branch: str,
    timestamp: str,
) -> dict[str, Any]:
    """
    Build a DynamoDB item from a test result dictionary.

    Args:
        test_data (dict): The parsed test result JSON.
        build_id (str): The CI build identifier.
        branch (str): The git branch name.
        timestamp (str): ISO 8601 timestamp for the sort key.

    Returns:
        dict: A DynamoDB-compatible item dictionary.
    """
    nodeid = test_data.get("nodeid", "unknown")
    test_name = extract_test_name(nodeid)
    test_file = extract_test_file(nodeid)
    browser = extract_browser(nodeid)

    setup = test_data.get("setup", {})
    call = test_data.get("call", {})
    teardown = test_data.get("teardown", {})

    setup_duration = setup.get("duration", 0.0)
    call_duration = call.get("duration", 0.0)
    teardown_duration = teardown.get("duration", 0.0)
    total_duration = setup_duration + call_duration + teardown_duration

    item: dict[str, Any] = {
        "test_id": f"TEST#{test_name}",
        "timestamp": timestamp,
        "nodeid": nodeid,
        "test_file": test_file,
        "test_name": test_name,
        "browser": browser,
        "outcome": test_data.get("outcome", "unknown"),
        "build_id": build_id,
        "branch": branch,
        "setup_outcome": setup.get("outcome", "unknown"),
        "setup_duration": to_decimal(setup_duration),
        "call_outcome": call.get("outcome", "unknown"),
        "call_duration": to_decimal(call_duration),
        "teardown_outcome": teardown.get("outcome", "unknown"),
        "teardown_duration": to_decimal(teardown_duration),
        "total_duration": to_decimal(total_duration),
    }

    # Add sparse crash attributes only if present
    item.update(extract_crash_info(test_data))

    return item


def upload_results(
    input_dir: str,
    build_id: str,
    branch: str,
    timestamp: str,
    dry_run: bool = False,
    endpoint_url: str | None = None
) -> None:
    """
    Loop through all JSON files in the input directory and upload each
    to DynamoDB.

    Args:
        input_dir (str): Directory containing individual test JSON files
        build_id (str): The CI build identifier.
        branch (str): The git branch name.
        timestamp (str): ISO 8601 timestamp string for the sort key.
        dry_run (bool): If True, print items instead of uploading.
        endpoint_url (str | None): If set, points at specific endpoint.
    """
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Error: Input directory not found: {input_dir}")
        sys.exit(1)

    json_files = list(input_path.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return

    if not dry_run:
        region = os.environ.get("AWS_REGION", DEFAULT_REGION)
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=region,
            endpoint_url=endpoint_url  # None by default = real AWS
        )
        table = dynamodb.Table(TABLE_NAME)

    items_to_upload = []

    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            test_data = json.load(f)

        item = build_dynamo_item(test_data, build_id, branch, timestamp)

        if dry_run:
            print(f"\n--- {json_file.name} ---")
            print(json.dumps(
                {k: str(v) for k, v in item.items()}, indent=4
            ))
        else:
            items_to_upload.append((json_file.name, item))

    if not dry_run:
        errors = 0
        try:
            with table.batch_writer() as batch:
                for filename, item in items_to_upload:
                    batch.put_item(Item=item)
                    print(f"Uploaded: {filename}")
        except Exception as e:
            print(f"Error during batch upload: {e}")
            errors += 1

        uploaded = len(items_to_upload) - errors
        print(f"\nUploaded {uploaded} item(s) to {TABLE_NAME}")
        if errors:
            print(f"{errors} error(s) encountered")
            sys.exit(1)


def main() -> None:
    """
    Main entry point. Parses arguments and triggers the upload.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Upload individual test result JSON files to DynamoDB"
        )
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default="test-results/json-output",
        help=(
            "Directory containing individual test JSON files "
            "(default: test-results/json-output)"
        )
    )
    parser.add_argument(
        "--build-id",
        type=str,
        default=os.environ.get("GITHUB_RUN_ID", "local"),
        help=(
            "Build ID to associate with results "
            "(default: GITHUB_RUN_ID env var or 'local')"
        )
    )
    parser.add_argument(
        "--branch",
        type=str,
        default=os.environ.get("GITHUB_REF_NAME", "local"),
        help=(
            "Branch name to associate with results "
            "(default: GITHUB_REF_NAME env var or 'local')"
        )
    )
    parser.add_argument(
        "--timestamp",
        type=str,
        default=datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        )[:-3] + "Z",
        help=(
            "ISO 8601 timestamp for the sort key "
            "(default: current UTC time)"
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print items without uploading to DynamoDB"
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

    args = parser.parse_args()

    upload_results(
        input_dir=args.input_dir,
        build_id=args.build_id,
        branch=args.branch,
        timestamp=args.timestamp,
        dry_run=args.dry_run,
        endpoint_url=args.endpoint_url
    )


if __name__ == "__main__":
    main()
