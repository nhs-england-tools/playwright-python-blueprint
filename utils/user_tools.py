import json
import logging
from pathlib import Path


logger = logging.getLogger(__name__)
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
        
        Returns:
            dict: A Python dictionary with the details of the user requested, if present.
        """
        with open(USERS_FILE, 'r') as file:
            user_data = json.loads(file.read())
        
        if not user in user_data:
            raise UserToolsException(f"User [{user}] is not present in users.json")
        
        logger.debug(f"Returning user: {user_data[user]}")
        return user_data[user]


class UserToolsException(Exception):
    pass
