"""
This script creates a local.env file that can be used to populate secrets such as passwords or API keys
locally. This is useful for local development and testing, as it allows you to keep sensitive information
out of your codebase.

This is designed to be generated when setting up this project, so if new variables are required, these
should be added to the REQUIRED_KEYS list below to automatically populate the local.env file with the
keys required to run this project.

The script itself can be executed using the following command from this directory:
    python setup_env_file.py

This can be run with the --empty flag to create the file with empty values for all keys, or without the
flag to attempt to populate values from the current environment variables (which will include any existing
local.env file if present).
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

REQUIRED_KEYS = [
    "# Authentication details",
    "USER_PASS",
    "",
    "# Jira / Confluence Configuration",
    "JIRA_URL",
    "JIRA_PROJECT_KEY",
    "JIRA_API_KEY",
    "JIRA_TICKET_REFERENCE",
    "CONFLUENCE_URL",
    "CONFLUENCE_API_KEY",
]
DEFAULT_LOCAL_ENV_PATH = Path(__file__).resolve().parent / "local.env"


def create_env_file(empty: bool = False):
    """
    Create a local.env file with the required keys.

    Args:
        empty (bool): If True, the file will be created with empty values for
            all keys. If False, it will attempt to populate values from the
            current environment variables by loading the existing local.env file.
    """
    if not empty:
        load_dotenv(DEFAULT_LOCAL_ENV_PATH, override=False)

    with open(DEFAULT_LOCAL_ENV_PATH, "w") as f:
        f.write(
            "# Use this file to populate secrets without committing them to the codebase (as this file is set in .gitignore).\n"
        )
        f.write(
            "# To retrieve values as part of your tests, use os.getenv('VARIABLE_NAME').\n"
        )
        f.write(
            "# Note: When running in a pipeline or workflow, you should pass these variables in at runtime.\n\n"
        )
        for key in REQUIRED_KEYS:
            if key.startswith("#"):  # This is a comment
                f.write(f"{key}\n")
            elif key == "":  # New line only
                f.write("\n")
            else:  # Expected key/value pair
                value = "" if empty else os.getenv(key, "")
                f.write(f"{key}={value}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--empty",
        action="store_true",
        help="Create the env file with empty values for all keys",
    )
    args = parser.parse_args()
    create_env_file(empty=args.empty)
