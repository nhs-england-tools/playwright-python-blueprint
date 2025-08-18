from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.table_util import TableUtils


class MaintainContactsPage(BasePage):
    """Maintain Contacts Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Maintain Contacts - page locators, methods

        self.surname_input_field = self.page.locator("#selPersonSurname")
        self.forenames_input_field = self.page.locator("#selPersonForenames")
        self.user_code_input_field = self.page.locator("#selUserCode")
        self.search_button = self.page.get_by_role("button", name="Search")

        self.search_table = TableUtils(self.page, "#displayRS")

    def verify_maintain_contacts_title(self) -> None:
        """Verify the Maintain Contacts page title is displayed correctly"""
        self.bowel_cancer_screening_page_title_contains_text("Maintain Contacts")

    def fill_surname_input_field(self, surname: str) -> None:
        """
        Fill the surname input field with the provided surname
        Args:
            surname (str): The surname of the subject
        """
        self.surname_input_field.fill(surname)

    def fill_forenames_input_field(self, forenames: str) -> None:
        """
        Fill the forenames input field with the provided forenames
        Args:
            forenames (str): The forenames of the subject
        """
        self.forenames_input_field.fill(forenames)

    def fill_user_code_input_field(self, user_code: str) -> None:
        """
        Fill the user code input field with the provided user code
        Args:
            user_code (str): The user code of the subject
        """
        self.user_code_input_field.fill(user_code)

    def click_search_button(self) -> None:
        """Click the search button to perform a search"""
        self.click(self.search_button)

    def click_person_link_from_surname(self, surname: str) -> None:
        """
        Clicks on the link containing the person's surname to go to the edit contact page
        Args:
            surname (str): The surname of the subject
        """
        self.click(self.page.get_by_role("link", name=surname).last)

    def click_person_link_from_forename(self, forename: str) -> None:
        """
        Clicks on the link containing the person's surname to go to the edit contact page
        Args:
            forename (str): The forename of the subject
        """
        self.click(self.page.get_by_role("link", name=forename).last)
