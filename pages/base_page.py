from playwright.sync_api import Page, expect, Locator, Dialog
import logging


class BasePage:
    """Base Page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        self.page = page
        # Homepage/Navigation Bar links
        self.sub_menu_link = self.page.get_by_role("link", name="Show Sub-menu")
        self.hide_sub_menu_link = self.page.get_by_role("link", name="Hide Sub-menu")
        self.select_org_link = self.page.get_by_role("link", name="Select Org")
        self.back_button = self.page.get_by_role("link", name="Back", exact=True)
        self.release_notes_link = self.page.get_by_role("link", name="- Release Notes")
        self.refresh_alerts_link = self.page.get_by_role("link", name="Refresh alerts")
        self.user_guide_link = self.page.get_by_role("link", name="User guide")
        self.help_link = self.page.get_by_role("link", name="Help")
        self.main_menu_link = self.page.get_by_role("link", name="Main Menu")
        self.log_out_link = self.page.get_by_role("link", name="Log-out")
        # Main menu - page links
        self.contacts_list_page = self.page.get_by_role("link", name="Contacts List")
        self.bowel_scope_page = self.page.get_by_role("link", name="Bowel Scope")
        self.call_and_recall_page = self.page.get_by_role(
            "link", name="Call and Recall"
        )
        self.communications_production_page = self.page.get_by_role(
            "link", name="Communications Production"
        )
        self.download_page = self.page.get_by_role("link", name="Download")
        self.fit_test_kits_page = self.page.get_by_role("link", name="FIT Test Kits")
        self.gfobt_test_kits_page = self.page.get_by_role(
            "link", name="gFOBT Test Kits"
        )
        self.lynch_surveillance_page = self.page.get_by_role(
            "link", name="Lynch Surveillance"
        )
        self.organisations_page = self.page.get_by_role("link", name="Organisations")
        self.reports_page = self.page.get_by_role("link", name="Reports")
        self.screening_practitioner_appointments_page = self.page.get_by_role(
            "link", name="Screening Practitioner Appointments"
        )
        self.screening_subject_search_page = self.page.get_by_role(
            "link", name="Screening Subject Search"
        )
        # Bowel Cancer Screening System header
        self.bowel_cancer_screening_system_header = self.page.locator("#ntshAppTitle")
        # Bowel Cancer Screening Page header
        self.bowel_cancer_screening_page_title = self.page.locator("#page-title")
        self.bowel_cancer_screening_ntsh_page_title = self.page.locator(
            "#ntshPageTitle"
        )
        self.main_menu__header = self.page.locator("#ntshPageTitle")

    def click_main_menu_link(self) -> None:
        """Click the Base Page 'Main Menu' link if it is visible."""
        if self.main_menu_link.is_visible():
            self.click(self.main_menu_link)

    def click_log_out_link(self) -> None:
        """Click the Base Page 'Log-out' link."""
        self.click(self.log_out_link)

    def click_sub_menu_link(self) -> None:
        """Click the Base Page 'Show Sub-menu' link."""
        self.click(self.sub_menu_link)

    def click_hide_sub_menu_link(self) -> None:
        """Click the Base Page 'Hide Sub-menu' link."""
        self.click(self.hide_sub_menu_link)

    def click_select_org_link(self) -> None:
        """Click the Base Page 'Select Org' link."""
        self.click(self.select_org_link)

    def click_back_button(self) -> None:
        """Click the Base Page 'Back' button."""
        self.click(self.back_button)

    def click_release_notes_link(self) -> None:
        """Click the Base Page 'Release Notes' link."""
        self.click(self.release_notes_link)

    def click_refresh_alerts_link(self) -> None:
        """Click the Base Page 'Refresh alerts' link."""
        self.click(self.refresh_alerts_link)

    def click_user_guide_link(self) -> None:
        """Click the Base Page 'User guide' link."""
        self.click(self.user_guide_link)

    def click_help_link(self) -> None:
        """Click the Base Page 'Help' link."""
        self.click(self.help_link)

    def bowel_cancer_screening_system_header_is_displayed(self) -> None:
        """Asserts that the Bowel Cancer Screening System header is displayed."""
        expect(self.bowel_cancer_screening_system_header).to_contain_text(
            "Bowel Cancer Screening System"
        )

    def main_menu_header_is_displayed(self) -> None:
        """Asserts that the Main Menu header is displayed."""
        expect(self.main_menu__header).to_contain_text("Main Menu")

    def bowel_cancer_screening_page_title_contains_text(self, text: str) -> None:
        """Asserts that the page title contains the specified text.

        Args:
            text (str): The expected text that you want to assert for the page title element.
        Page elements of interest:
            self.bowel_cancer_screening_page_title
            self.bowel_cancer_screening_ntsh_page_title
        """
        self.page.wait_for_load_state("load")
        self.page.wait_for_load_state("domcontentloaded")
        if self.bowel_cancer_screening_page_title.is_visible():
            expect(self.bowel_cancer_screening_page_title).to_contain_text(text)
        else:
            expect(self.bowel_cancer_screening_ntsh_page_title).to_contain_text(text)

    def go_to_contacts_list_page(self) -> None:
        """Click the Base Page 'Contacts List' link."""
        self.click(self.contacts_list_page)

    def go_to_bowel_scope_page(self) -> None:
        """Click the Base Page 'Bowel Scope' link."""
        self.click(self.bowel_scope_page)

    def go_to_call_and_recall_page(self) -> None:
        """Click the Base Page 'Call and Recall' link."""
        self.click(self.call_and_recall_page)

    def go_to_communications_production_page(self) -> None:
        """Click the Base Page 'Communications Production' link."""
        self.click(self.communications_production_page)

    def go_to_download_page(self) -> None:
        """Click the Base Page 'Download' link."""
        self.click(self.download_page)

    def go_to_fit_test_kits_page(self) -> None:
        """Click the Base Page 'FIT Test Kits' link."""
        self.click(self.fit_test_kits_page)

    def go_to_gfobt_test_kits_page(self) -> None:
        """Click the Base Page 'gFOBT Test Kits' link."""
        self.click(self.gfobt_test_kits_page)

    def go_to_lynch_surveillance_page(self) -> None:
        """Click the Base Page 'Lynch Surveillance' link."""
        self.click(self.lynch_surveillance_page)

    def go_to_organisations_page(self) -> None:
        """Click the Base Page 'Organisations' link."""
        self.click(self.organisations_page)

    def go_to_reports_page(self) -> None:
        """Click the Base Page 'Reports' link."""
        self.click(self.reports_page)

    def go_to_screening_practitioner_appointments_page(self) -> None:
        """Click the Base Page 'Screening Practitioner Appointments' link."""
        self.click(self.screening_practitioner_appointments_page)

    def go_to_screening_subject_search_page(self) -> None:
        """Click the Base Page 'Screening Subject Search' link."""
        self.click(self.screening_subject_search_page)

    def click(self, locator: Locator) -> None:
        # Alerts table locator
        alerts_table = locator.get_by_role("table", name="cockpitalertbox")
        """
        This is used to click on a locator
        The reason for this being used over the normal playwright click method is due to:
        - BCSS sometimes takes a while to render and so the normal click function 'clicks' on a locator before its available
        - Increases the reliability of clicks to avoid issues with the normal click method
        """
        if alerts_table.is_visible():
            alerts_table.wait_for(state="attached")
            alerts_table.wait_for(state="visible")

        try:
            self.page.wait_for_load_state("load")
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_load_state("networkidle")
            locator.wait_for(state="attached")
            locator.wait_for(state="visible")
            locator.click()

        except Exception as locatorClickError:
            logging.warning(
                f"Failed to click element with error: {locatorClickError}, trying again..."
            )
            locator.click()

    def _accept_dialog(self, dialog: Dialog) -> None:
        """
        This method is used to accept dialogs
        If it has already been accepted then it is ignored
        """
        try:
            dialog.accept()
        except Exception:
            logging.warning("Dialog already handled")

    def safe_accept_dialog(self, locator: Locator) -> None:
        """
        Safely accepts a dialog triggered by a click, avoiding the error:
        playwright._impl._errors.Error: Dialog.accept: Cannot accept dialog which is already handled!
        If no dialog appears, continues without error.
        """
        self.page.once("dialog", self._accept_dialog)
        try:
            self.click(locator)
        except Exception as e:
            logging.error(f"Click failed: {e}")
