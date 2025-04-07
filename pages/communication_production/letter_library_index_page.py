from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LetterLibraryIndex(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Letter Library Index - page locators
        self.letter_library_index_title = self.page.locator("#ntshPageTitle")

    def verify_letter_library_index_title(self) -> None:
        expect(self.letter_library_index_title).to_contain_text("Letter Library Index")
