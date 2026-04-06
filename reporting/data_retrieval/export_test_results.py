"""
This script extracts individual test results from results.json and
creates separate JSON files for each test in the json-output directory.

The script reads the test-results/results.json file and creates
individual JSON files for each test case, saving them to
test-results/json-output/ with filenames based on the test file and
test name.

The script can be executed using the following command:
    python reporting/export_test_results.py

The following arguments are supported:
    --results-file <path> = Path to the results.json file. Defaults to
                            test-results/results.json
    --output-dir <path> = Directory to output individual JSON files.
                          Defaults to test-results/json-output
"""

import argparse
import json
import os
import re
from pathlib import Path


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a string to be safe for use as a filename.

    Args:
        filename (str): The string to sanitize.

    Returns:
        str: A sanitized filename safe for filesystem use.
    """
    # Replace special characters with underscores
    sanitized = re.sub(r'[^\w\-.]', '_', filename)
    # Remove consecutive underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    return sanitized


def extract_test_info(nodeid: str) -> tuple[str, str]:
    """
    Extract test file and test name from a test nodeid.

    Args:
        nodeid (str): The test nodeid (e.g.,
            "tests/test_example.py::test_basic_example[chromium]")

    Returns:
        tuple[str, str]: A tuple containing (test_file, test_name).
    """
    # Split on :: to separate file path from test name
    parts = nodeid.split('::')
    file_path = parts[0] if len(parts) > 0 else 'unknown'
    test_name = parts[1] if len(parts) > 1 else 'unknown'

    # Extract just the filename without path and extension
    test_file = Path(file_path).stem

    return test_file, test_name


def export_individual_test_results(
    results_file: str,
    output_dir: str
) -> None:
    """
    Export individual test results from results.json to separate JSON
    files.

    Args:
        results_file (str): Path to the results.json file.
        output_dir (str): Directory to output individual JSON files.
    """
    # Check if results file exists
    if not os.path.exists(results_file):
        print(f"Error: Results file not found at {results_file}")
        return

    # Read the results.json file
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Check if tests exist in the results
    if 'tests' not in results or not results['tests']:
        print("No tests found in results.json")
        return

    # Extract and save each test
    for test in results['tests']:
        nodeid = test.get('nodeid', 'unknown')
        test_file, test_name = extract_test_info(nodeid)

        # Create a sanitized filename
        filename = sanitize_filename(f"{test_file}_{test_name}")
        output_path = os.path.join(output_dir, f"{filename}.json")

        # Write the individual test result to a JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(test, f, indent=4)

        print(f"Exported: {filename}.json")

    print(f"\nSuccessfully exported {len(results['tests'])} test(s) "
          f"to {output_dir}")


def main() -> None:
    """
    Main entry point for the script.
    Parses command line arguments and initiates the export process.
    """
    parser = argparse.ArgumentParser(
        description='Export individual test results from results.json'
    )
    parser.add_argument(
        '--results-file',
        type=str,
        default='test-results/results.json',
        help='Path to the results.json file '
             '(default: test-results/results.json)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='test-results/json-output',
        help='Directory to output individual JSON files '
             '(default: test-results/json-output)'
    )

    args = parser.parse_args()

    export_individual_test_results(args.results_file, args.output_dir)


if __name__ == '__main__':
    main()
