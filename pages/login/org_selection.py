import logging
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


PAGE_HEADER = "Choose Organisation"


class OrgSelectionPage(BasePage):

    def __init__(self, page: Page) -> None:
        BasePage.__init__(self, page)
        self.page = page

    def org_selection(self, role: str = None) -> None:
        self.page.wait_for_selector("h1.bss-page-title")
        if self.page.url.endswith("/bss/orgChoice"):
            self.verify_header()
            if role is not None:
                logging.info(f"Selecting role: {role}")
                options = self.page.locator("#chosenOrgCode option").all()
                for option in options:
                    if option.get_attribute("value") == role:
                        self.page.locator("#chosenOrgCode").select_option(role)
                        break
                else:
                    raise AssertionError(
                        f"Role '{role}' not found on /orgChoice screen."
                    )

            self.page.get_by_role("button", name="Select Organisation").click()

    def verify_header(self, header: str = PAGE_HEADER) -> None:
        return super().verify_header(header)
