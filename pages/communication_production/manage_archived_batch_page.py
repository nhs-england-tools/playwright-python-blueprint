from playwright.sync_api import Page
from pages.base_page import BasePage
from playwright.sync_api import expect


class ManageArchivedBatchPage(BasePage):
    """Page object for the Manage Archived Batch Screen."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.reprint_button = self.page.locator(
            "input.ReprintButton[value='Reprint Batch']"
        )
        self.confirmation_msg = self.page.locator(
            'text="Batch Successfully Archived and Printed"'
        )

    def assert_archived_batch_details_visible(self) -> None:
        """Verifies the Manage Archived Batch page has loaded."""
        expect(self.bowel_cancer_screening_page_title).to_have_text("Manage Archived Batch")

    def click_reprint_button(self) -> None:
        """Clicks the 'Reprint' button on the Archived Batch details page."""
        expect(self.reprint_button).to_be_visible()
        self.reprint_button.click()

    def confirm_archived_message_visible(self) -> None:
        """Verifies that the batch was successfully archived and confirmation message is shown."""
        expect(self.confirmation_msg).to_be_visible()
