import json
import os
import logging
from pathlib import Path

USERS_FILE = Path(__file__).parent.parent / "users.json"


class UserTools:
    """
    A utility class for retrieving and doing common actions with users.
    """

    @staticmethod
    def retrieve_user(user: str) -> dict:
        """
        Retrieves the user information as a dict for the user provided.

        Args:
            user (str): The user details required, using the record key from users.json.
        """
        with open(USERS_FILE, 'r') as file:
            user_data = json.loads(file.read())
        
        if not user in user_data:
            raise Exception(f"User [{user}] is not present in users.json")
        
        return user_data[user]
