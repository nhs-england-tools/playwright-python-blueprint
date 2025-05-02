from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ContactsListPage(BasePage):
    """Contacts List Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # ContactsList Page
        self.view_contacts_page = self.page.get_by_role("link", name="View Contacts")
        self.edit_my_contact_details_page = self.page.get_by_role(
            "link", name="Edit My Contact Details"
        )
        self.maintain_contacts_page = self.page.get_by_role(
            "link", name="Maintain Contacts"
        )
        self.my_preference_settings_page = self.page.get_by_role(
            "link", name="My Preference Settings"
        )
        self.extract_contact_details_page = self.page.get_by_text(
            "Extract Contact Details"
        )
        self.resect_and_discard_accredited_page = self.page.get_by_text(
            "Resect and Discard Accredited"
        )

    def go_to_view_contacts_page(self) -> None:
        """Click the View Contacts link"""
        self.click(self.view_contacts_page)

    def go_to_edit_my_contact_details_page(self) -> None:
        """Click the Edit My Contact Details link"""
        self.click(self.edit_my_contact_details_page)

    def go_to_maintain_contacts_page(self) -> None:
        """Click the Maintain Contacts link"""
        self.click(self.maintain_contacts_page)

    def go_to_my_preference_settings_page(self) -> None:
        """Click the My Preference Settings link"""
        self.click(self.my_preference_settings_page)

    def verify_extract_contact_details_page_visible(self) -> None:
        """Verify the Extract Contact Details page is visible"""
        expect(self.extract_contact_details_page).to_be_visible()

    def verify_resect_and_discard_accredited_page_visible(self) -> None:
        """Verify the Resect and Discard Accredited page is visible"""
        expect(self.resect_and_discard_accredited_page).to_be_visible()
