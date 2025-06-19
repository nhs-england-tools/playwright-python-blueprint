import logging
from playwright.sync_api import Page, expect


class CognitoAuthenticationPage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def cognito_login(self, username: str, password: str) -> None:
        logging.info(f"Logging in as: {username}")
        self.page.get_by_role("textbox", name="Username").fill(username)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="submit").click()
