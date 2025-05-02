import os
from playwright.sync_api import Page
from utils.user_tools import UserTools
from pages.base_page import BasePage
from dotenv import load_dotenv


class BcssLoginPage(BasePage):
    """Login Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.page.goto("/")
        self.username = self.page.get_by_role("textbox", name="Username")
        self.password = self.page.get_by_role("textbox", name="Password")
        self.submit_button = self.page.get_by_role("button", name="submit")
        load_dotenv()  # Take environment variables from .env

    def login_as_user(self, username: str) -> None:
        """Logs in to bcss with specified user credentials
        Args:
            username (str) enter a username that exists in users.json
        """
        # Retrieve and enter username from users.json
        user_details = UserTools.retrieve_user(username)
        self.username.fill(user_details["username"])
        # Retrieve and enter password from .env file
        password = os.getenv("BCSS_PASS")
        self.password.fill(password)
        # Click Submit
        self.click(self.submit_button)
