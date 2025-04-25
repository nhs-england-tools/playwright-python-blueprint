"""
This script creates a local.env file that can be used to populate secrets such as passwords or API keys
locally. This is useful for local development and testing, as it allows you to keep sensitive information
out of your codebase.

This is designed to be generated when setting up this project, so if new variables are required, these
should be added to the REQUIRED_KEYS list below to automatically populate the local.env file with the
keys required to run this project.
"""

import os
from pathlib import Path

REQUIRED_KEYS = ["USER_PASS"]
DEFAULT_LOCAL_ENV_PATH = Path(os.getcwd()) / 'local.env'

def create_env_file():
    """
    Create a local.env file with the required keys.
    """
    with open(DEFAULT_LOCAL_ENV_PATH, 'w') as f:
        f.write("# Use this file to populate secrets without committing them to the codebase (as this file is set in .gitignore).\n")
        f.write("# To retrieve values as part of your tests, use os.getenv('VARIABLE_NAME').\n")
        f.write("# Note: When running in a pipeline or workflow, you should pass these variables in at runtime.\n\n")
        for key in REQUIRED_KEYS:
            f.write(f'{key}=\n')


if __name__ == "__main__":
    create_env_file()
