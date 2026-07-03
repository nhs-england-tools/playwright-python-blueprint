"""
This script allows for the uploading of files to Jira once a test run has been completed and the test-results/ directory
has been populated. This script is designed to work locally (when building tests) and via a pipeline or workflow during
CI/CD operations.

The following environment variables need to be set (in local.env if running locally) before this can upload any files:
    - JIRA_URL: The Jira instance to upload to.
    - JIRA_PROJECT_KEY: The Jira project key that should be uploaded to.
    - JIRA_API_KEY: The API key to use to complete actions. Locally you should generate your own key, and use a bot in a pipeline/workflow.

The following environment variables are optional:
    - JIRA_TICKET_REFERENCE: The Jira ticket to push to if set. If not, will attempt to derive the value from the git branch.

The script itself can be executed using the following command:
    python jira_upload.py

The following arguments are supported in addition:
    --jira-ref <Jira Reference> = The Jira ticket to upload to. Will take precedence over auto-deriving from branch name and the set environment variable.
    --results-dir <Directory> = The directory to point to. If not set, points to test-results/ in this directory.
    --no-html = Don't include HTML files in the upload.
    --no-trace = Don't include Trace files (.zip) in the upload.
    --no-csv = Don't include CSV files in the upload.
    --no-screenshots = Don't include screenshots (.png) in the upload.
    --no-comment = Don't add a Jira comment highlighting the results.
    --no-env-data = Don't include environment data in the Jira comment.
    --overwrite-files = If a filename exists on the ticket that matches those in the results directory, overwrite them.
    --auto-confirm = Will not ask if you want to proceed if set, and will assume that yes has been pressed.
"""

import argparse
import sys
from utils.jira_confluence_util import JiraConfluenceUtil


def upload_jira_files(args: argparse.Namespace) -> None:
    """
    This checks the arguments passed in and calls the logic to upload the data from the test-results directory to
    Jira.
    """
    try:
        jira_instance = (
            JiraConfluenceUtil()
            if args.results_dir is None
            else JiraConfluenceUtil(results_dir=args.results_dir)
        )

        if args.jira_ref is not None:
            jira_ref = (
                args.jira_ref
                if jira_instance.is_valid_jira_reference(args.jira_ref)
                else ""
            )
        else:
            jira_ref = jira_instance.determine_jira_reference_local()

        if not jira_ref:
            raise ValueError("ERROR: Cannot proceed due to invalid Jira reference")

        jira_instance.upload_test_results_dir_to_jira(
            ticket_id=jira_ref,
            overwrite_files=args.overwrite_files,
            include_html=not args.no_html,
            include_trace_files=not args.no_trace,
            include_screenshots=not args.no_screenshots,
            include_csv=not args.no_csv,
            include_env_metadata=not args.no_env_data,
            add_comment=not args.no_comment,
            automatically_accept=args.auto_confirm,
        )
    except Exception as e:
        print("An error has been encountered so exiting upload process")
        print(f"{e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload test results from the test-results directory."
    )
    parser.add_argument(
        "--jira-ref", type=str, help="Specify the Jira reference to upload to"
    )
    parser.add_argument(
        "--results-dir", type=str, help="Specify the results directory to upload from"
    )
    parser.add_argument(
        "--no-html", action="store_true", help="Don't include HTML files in upload"
    )
    parser.add_argument(
        "--no-trace", action="store_true", help="Don't include trace files"
    )
    parser.add_argument("--no-csv", action="store_true", help="Don't include CSV files")
    parser.add_argument(
        "--no-screenshots", action="store_true", help="Don't include screenshots"
    )
    parser.add_argument(
        "--no-comment", action="store_true", help="Don't include a comment"
    )
    parser.add_argument(
        "--no-env-data",
        action="store_true",
        help="Don't include environment metadata in comment",
    )
    parser.add_argument(
        "--overwrite-files",
        action="store_true",
        help="If files are already on the Jira ticket with the same name, overwrite them with this file.",
    )
    parser.add_argument(
        "--auto-confirm",
        action="store_true",
        help="Don't prompt to confirm actions before proceeding",
    )
    args = parser.parse_args()
    upload_jira_files(args)
