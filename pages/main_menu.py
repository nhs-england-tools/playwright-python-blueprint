import logging
from playwright.sync_api import Page
from pages.base_page import BasePage


HEADER = "Welcome to Breast Screening Select"


class MainMenuPage(BasePage):

    def __init__(self, page: Page) -> None:
        self.page = page

    def verify_header(self) -> None:
        return super().verify_header(HEADER)
