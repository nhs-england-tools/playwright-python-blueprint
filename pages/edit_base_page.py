from playwright.sync_api import Page, TimeoutError as playwrightTimeoutError
from pages.base_page import BasePage


class EditBasePage(BasePage):
    def __init__(self, page: Page) -> None:
        BasePage.__init__(self, page)

    def save_clinical_content(
        self, target_release: str, author_note: str, release_box_type: str = ""
    ) -> None:
        """
        This method clicks Save on a clinical item, populates data on the Change History Modal then saves the changes.
        """
        self.page.get_by_role("button", name="Save").click()
        match release_box_type:
            case "questions":
                self.page.get_by_role("dialog", name="Change history detail").get_by_label("Select target release").select_option(target_release)
            case "conditions":
                self.page.get_by_role("dialog", name="Change history detail").get_by_label("Releases").select_option("42.2.0")
            case _:
                self.page.get_by_label("Target Release *").select_option(target_release)

        self.page.get_by_role("textbox", name="Author note", exact=True).fill(author_note)
        self.page.get_by_role("button", name="Save Changes", exact=True).click()

    def click_change_history_log(self) -> None:
        """
        This method clicks on the latest log from author "Automated PW Team Member" in the change history table.
        """
        self.page.get_by_role("cell", name="Automated PW Team Member").first.click()
