import logging
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


PAGE_HEADER = "Choose Organisation"


class OrgSelectionPage(BasePage):

    def __init__(self, page: Page) -> None:
        BasePage.__init__(self, page)
        self.page = page

    def org_selection(self, role: str = None) -> None:
        expect(self.page.get_by_text("Breast Screening Select")).to_be_visible()
        if self.page.url.endswith("/bss/orgChoice"):
            self.verify_header()
            if role is not None:
                logging.info(f"Selecting role: {role}")
                self.page.locator("#chosenOrgCode").select_option(role)
            self.page.get_by_role("button", name="Select Organisation").click()

    def verify_header(self) -> None:
        return super().verify_header(PAGE_HEADER)
