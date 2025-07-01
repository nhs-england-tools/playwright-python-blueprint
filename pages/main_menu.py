import logging
from playwright.sync_api import Page
from pages.base_page import BasePage


HEADER = "Welcome to Breast Screening Select"


class MainMenuPage(BasePage):

    def __init__(self, page: Page) -> None:
        BasePage.__init__(self, page)

    def verify_header(self, header: str = HEADER) -> None:
        return super().verify_header(header)
