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
        self.cancer_audit_show_dataset_button = (
            self.page.locator("div")
            .filter(has_text="Cancer Audit (1 Dataset) Show")
            .get_by_role("link")
        )
        self.add_link = self.page.get_by_role("link", name="Add")

    def click_add_link(self) -> None:
        """Clicks on the 'Add' link on the Subject Datasets Page."""
        self.click(self.add_link)

    def click_colonoscopy_show_datasets(self) -> None:
        """Clicks on the 'Show Dataset' button for the Colonoscopy Assessment row on the Subject Datasets Page."""
        self.click(self.colonoscopy_show_dataset_button)

    def click_investigation_show_datasets(self) -> None:
        """
        Clicks on the 'Show Dataset(s)' link for the Investigation row on the Subject Datasets Page.
        If the button text is "Show Datasets", also clicks the 'Add' link.
        """
        # Find the DatasetHeader div with Investigation
        header = self.page.locator("div.DatasetHeader h4:has-text('Investigation')")
        header.wait_for(state="visible", timeout=10000)
        # Get the dataset count text from the span inside the h4
        dataset_count_text = header.locator("span.DatasetSubLabel").text_content()
        # Go up to the parent container (likely the row), then find the Show Dataset(s) link
        container = header.locator(
            "xpath=ancestor::div[contains(@class, 'DatasetTitle')]/following-sibling::div[contains(@class, 'DatasetLink')]"
        )
        show_link = container.locator("a:has-text('Show Dataset')")
        show_link.wait_for(state="visible", timeout=10000)
        self.click(show_link)
        # If plural, also click Add
        if dataset_count_text and "2 Datasets" in dataset_count_text:
            self.click_add_link()

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

    def click_cancer_audit_show_datasets(self) -> None:
        """Clicks on the 'Show Dataset' button for the Cancer Audit row on the Subject Datasets Page."""
        self.click(self.cancer_audit_show_dataset_button)
