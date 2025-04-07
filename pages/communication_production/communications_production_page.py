from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CommunicationsProduction(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Communication Production - page links
        self.active_batch_list_page = self.page.get_by_role(
            "link", name="Active Batch List"
        )
        self.archived_batch_list_page = self.page.get_by_role(
            "link", name="Archived Batch List"
        )
        self.letter_library_index_page = self.page.get_by_role(
            "link", name="Letter Library Index"
        )
        self.letter_signatory_page = self.page.get_by_role(
            "link", name="Letter Signatory"
        )
        self.electronic_communication_management_page = self.page.get_by_role(
            "link", name="Electronic Communication Management"
        )
        self.manage_individual_letter_page = self.page.get_by_text(
            "Manage Individual Letter"
        )

    def verify_manage_individual_letter_page_visible(self) -> None:
        expect(self.manage_individual_letter_page).to_be_visible()

    def go_to_active_batch_list_page(self) -> None:
        self.click(self.active_batch_list_page)

    def go_to_archived_batch_list_page(self) -> None:
        self.click(self.archived_batch_list_page)

    def go_to_letter_library_index_page(self) -> None:
        self.click(self.letter_library_index_page)

    def go_to_letter_signatory_page(self) -> None:
        self.click(self.letter_signatory_page)

    def go_to_electronic_communication_management_page(self) -> None:
        self.click(self.electronic_communication_management_page)
