import os
import json
from datetime import date
from typing import Dict, Any, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LAST_RUN_FILE = os.path.join(PROJECT_ROOT, ".test_last_runs.json")


def load_last_run_data() -> Dict[str, Any]:
    """
    Loads the last run data from the JSON file.

    Returns:
        Dict[str, Any]: A dictionary mapping environments to test names and their last run date.
    """
    if os.path.exists(LAST_RUN_FILE):
        try:
            with open(LAST_RUN_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_last_run_data(data: Dict[str, Any]) -> None:
    """
    Saves the last run data to the JSON file.

    Args:
        data (Dict[str, Any]): The data to save, mapping environments to test names and their last run date.
    """
    with open(LAST_RUN_FILE, "w") as f:
        json.dump(data, f, indent=2)


def has_test_run_today(test_name: str, base_url: Optional[str] = None) -> bool:
    """
    Checks if the given test has already run today in the given environment.
    If not, updates the record to mark it as run today for that environment.

    Args:
        test_name (str): The name of the test to check.
        base_url (str, optional): The environment base URL.

    Returns:
        bool: True if the test has already run today in this environment, False otherwise.
    """
    data = load_last_run_data()
    today = date.today().isoformat()
    env = base_url or "unknown"

    # Ensure the environment key exists
    env_data = data.get(env, {})

    # Check if the test has run today in this environment
    last_run = env_data.get(test_name, {})
    if last_run.get("date") == today:
        return True
    else:
        # Update only the relevant environment/test combination
        if env not in data:
            data[env] = {}
        data[env][test_name] = {"date": today}
        save_last_run_data(data)
        return False
