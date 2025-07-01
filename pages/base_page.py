import logging
from playwright.sync_api import Page, expect


class BasePage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.menu_bar = self.page.locator("#bss-menu-bar")

    def verify_header(self, header: str) -> None:
        expect(self.page.get_by_role("heading")).to_contain_text(header)

    def select_menu_option(self, menu_option: str, sub_menu_option: str = "") -> None:
        if sub_menu_option == "":
            self.menu_bar.get_by_role("link", name=menu_option).click()
            logging.info(f"Navigated to: {menu_option}")
        else:
            self.menu_bar.get_by_text(menu_option).hover()
            self.menu_bar.get_by_role("link", name=sub_menu_option).click()
            logging.info(f"Navigated to: {menu_option} -> {sub_menu_option}")

    def logout(self) -> None:
        self.page.get_by_role("link", name="Logout").click()
