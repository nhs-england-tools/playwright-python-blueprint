from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class SubjectDatasetsPage(BasePage):
    """Subject Datasets Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Subject datasets page locators
        self.colonoscopy_show_dataset_button = (
            self.page.locator("div")
            # Note: The "(1 Dataset)" part of the line below may be dynamic and may change based on the actual dataset count.
            .filter(
                has_text="Colonoscopy Assessment (1 Dataset) Show Dataset"
            ).get_by_role("link")
        )
        self.investigation_show_dataset_button = (
            self.page.locator("div")
            # Note: The "(1 Dataset)" part of the line below may be dynamic and may change based on the actual dataset count.
            .filter(has_text="Investigation (1 Dataset) Show Dataset").get_by_role(
                "link"
            )
        )

    def click_colonoscopy_show_datasets(self) -> None:
        """Clicks on the 'Show Dataset' button for the Colonoscopy Assessment row on the Subject Datasets Page."""
        self.click(self.colonoscopy_show_dataset_button)

    def click_investigation_show_datasets(self) -> None:
        """Clicks on the 'Show Dataset' button for the Investigation row on the Subject Datasets Page."""
        self.click(self.investigation_show_dataset_button)

    def check_investigation_dataset_complete(self) -> None:
        """
        Verify that the investigation dataset is marked as complete.

        """
        expect(
            self.page.locator(
                "h4:has-text('Investigation') span.softHighlight",
                has_text="** Completed **",
            )
        ).to_be_visible()
