import json
import os
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import Page
from pages.login.cognito_login_page import CognitoLoginPage
from classes.user import User
from classes.organisation import Organisation

logger = logging.getLogger(__name__)
USERS_FILE = Path(os.getcwd()) / "users.json"


class UserTools:
    """
    A utility class for retrieving and doing common actions with users.
    """

    @staticmethod
    def user_login(page: Page, username: str) -> None:
        """
        Logs into the BCSS application as a specified user.

        Args:
            page (playwright.sync_api.Page): The Playwright page object to interact with.
            username (str): Enter a username that exists in the users.json file.
        """
        logging.info(f"Logging in as {username}")
        # Go to base url
        page.goto("/")
        # Retrieve username from users.json
        user_details = UserTools.retrieve_user(username)
        # Login to bcss using retrieved username and a password stored in the .env file
        password = os.getenv("BCSS_PASS")
        if password is None:
            raise ValueError("Environment variable 'BCSS_PASS' is not set")
        CognitoLoginPage(page).login_as_user(user_details["username"], password)

    @staticmethod
    def retrieve_user(user: str) -> dict:
        """
        Retrieves the user information as a dict for the user provided.

        Args:
            user (str): The user details required, using the record key from users.json.

        Returns:
            dict: A Python dictionary with the details of the user requested, if present.
        """
        with open(USERS_FILE, "r") as file:
            user_data = json.loads(file.read())

        if user not in user_data:
            raise UserToolsException(f"User [{user}] is not present in users.json")

        logger.debug(f"Returning user: {user_data[user]}")
        return user_data[user]

    @staticmethod
    def get_user_object(user_details: dict) -> User:
        """
        Converts a user_details dictionary into a User object.

        Args:
            user_details (dict): Dictionary containing user attributes.

        Returns:
            User: A User object with populated fields.
        """
        raw_org_id = user_details.get("organisation_id") or user_details.get("hub_code")
        org_id = str(raw_org_id) if raw_org_id is not None else "UNKNOWN_ORG"

        organisation = Organisation(organisation_id=org_id)

        user_id = user_details.get("user_id", 9999)
        user = User(user_id=user_id, organisation=organisation)

        return user


class UserToolsException(Exception):
    pass
