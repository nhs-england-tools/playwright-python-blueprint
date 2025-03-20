import os

from playwright.sync_api import Page


class CognitoLoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_role("textbox", name="Username")
        self.password = page.get_by_role("textbox", name="Password")
        self.submit_button = page.get_by_role("button", name="submit")

    def login_as_user(self, username: str, password: str) -> None:
        """Logs in to bcss with specified user credentials
        Args:
            username (str) enter a username that exists in users.json
            password (str) the password for the user provided
        """
        # Retrieve and enter username from users.json
        self.username.fill(username)
        # Retrieve and enter password from .env file
        self.password.fill(password)
        # Click Submit
        self.submit_button.click()
