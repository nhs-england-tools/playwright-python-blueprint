from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class LetterSignatory(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        #Letter Signatory - page locators
        self.letter_signatory_title = self.page.locator("#ntshPageTitle")

    def verify_letter_signatory_title(self) -> None:
        expect(self.letter_signatory_title).to_contain_text("Letter Signatory")
