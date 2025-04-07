from playwright.sync_api import Page
from pages.base_page import BasePage


class ManageActiveBatch(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Manage Active Batch - page buttons
        self.prepare_button = self.page.get_by_role("button", name="Prepare Batch")
        self.retrieve_button = self.page.get_by_role("button", name="Retrieve")
        self.confirm_button = self.page.get_by_role("button", name="Confirm Printed")
        # Manage Active Batch - page buttons (text)
        self.prepare_button_text = self.page.locator('text="Prepare Batch"')
        self.retrieve_button_text = self.page.locator('text="Retrieve"')
        self.confirm_button_text = self.page.locator('text="Confirm Printed"')
        self.reprepare_batch_text = self.page.locator('text="Re-Prepare Batch"')

    def click_prepare_button(self) -> None:
        self.click(self.prepare_button)

    def click_retrieve_button(self) -> None:
        self.click(self.retrieve_button)

    def click_confirm_button(self) -> None:
        self.click(self.confirm_button)
