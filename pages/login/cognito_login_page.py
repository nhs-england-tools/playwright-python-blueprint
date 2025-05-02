from playwright.sync_api import Page
from pages.base_page import BasePage


class CognitoLoginPage(BasePage):
    """Cognito Login Page locators, and methods for logging in to bcss via the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.username = self.page.get_by_role("textbox", name="Username")
        self.password = self.page.get_by_role("textbox", name="Password")
        self.submit_button = self.page.get_by_role("button", name="submit")

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
        self.click(self.submit_button)
