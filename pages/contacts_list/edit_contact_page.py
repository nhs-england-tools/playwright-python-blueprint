from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.table_util import TableUtils


class EditContactPage(BasePage):
    """Edit Contact Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Edit Contact - page locators, methods
        self.view_resect_and_discard_link = self.page.get_by_role(
            "link", name="View Resect and Discard"
        )

        self.edit_contact_table = TableUtils(self.page, "#displayRS")

    def click_view_resect_and_discard_link(self) -> None:
        """Clicks on the 'View Resect and Discard' link"""
        self.click(self.view_resect_and_discard_link)

    def assert_value_for_label_in_edit_contact_table(
        self, label_text: str, expected_text: str
    ) -> None:
        """
        Asserts that the vlaue for a label is as expected in the edit contact table

        Args:
            label_text (str): The label text to look for in the first cell of a row.
            expected_text (str): The text expected inside the adjacent cell.
        """
        self.edit_contact_table.verify_value_for_label(label_text, expected_text)
