from playwright.sync_api import Page, expect, Locator, Dialog
import logging


class BasePage:
    """Base Page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        self.page = page
        # Homepage - vars
        self.main_menu_string = "Main Menu"
        # Homepage/Navigation Bar links
        self.sub_menu_link = self.page.get_by_role("link", name="Show Sub-menu")
        self.hide_sub_menu_link = self.page.get_by_role("link", name="Hide Sub-menu")
        self.select_org_link = self.page.get_by_role("link", name="Select Org")
        self.back_button = self.page.get_by_role("link", name="Back", exact=True)
        self.release_notes_link = self.page.get_by_role("link", name="- Release Notes")
        self.refresh_alerts_link = self.page.get_by_role("link", name="Refresh alerts")
        self.user_guide_link = self.page.get_by_role("link", name="User guide")
        self.help_link = self.page.get_by_role("link", name="Help")
        self.main_menu_link = self.page.get_by_role("link", name=self.main_menu_string)
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
        self.log_in_page = self.page.get_by_role("button", name="Log in")
        # Bowel Cancer Screening System header
        self.bowel_cancer_screening_system_header = self.page.locator("#ntshAppTitle")
        # Bowel Cancer Screening Page header
        self.bowel_cancer_screening_page_title = self.page.locator("#page-title")
        self.bowel_cancer_screening_ntsh_page_title = self.page.locator(
            "#ntshPageTitle"
        )
        self.main_menu_header = self.page.locator("#ntshPageTitle")

    def click_main_menu_link(self) -> None:
        """Click the Base Page 'Main Menu' link if it is visible."""
        loops = 0
        text = None

        while loops <= 3:
            if self.main_menu_link.is_visible():
                self.click(self.main_menu_link)
            try:
                if self.main_menu_header.is_visible():
                    text = self.main_menu_header.text_content()
                else:
                    text = None
            except Exception as e:
                logging.warning(f"Could not read header text: {e}")
                text = None

            if text and self.main_menu_string in text:
                return  # Success
            else:
                logging.warning("Main Menu click failed, retrying after 0.2 seconds")
                # The timeout is in place here to allow the page ample time to load if it has not already been loaded
                self.page.wait_for_timeout(200)

            loops += 1
        # All attempts failed
        raise RuntimeError(
            f"Failed to navigate to Main Menu after {loops} attempts. Last page title was: '{text or 'unknown'}'"
        )

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
        """
        Asserts that the Main Menu header is displayed.
        self.main_menu_string contains the string 'Main Menu'
        """
        expect(self.main_menu_header).to_contain_text(self.main_menu_string)

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
        Safely accepts a dialog triggered by a click, logging its contents.
        Avoids the error: Dialog.accept: Cannot accept dialog which is already handled!
        If no dialog appears, continues without error.
        Args:
            locator (Locator): The locator that triggers the dialog when clicked.
        """

        def handle_dialog(dialog: Dialog):
            try:
                logging.info(f"[DIALOG APPEARED WITH MESSAGE]: {dialog.message}")
                dialog.accept()
            except Exception:
                logging.warning("Dialog already accepted or handled")

        self.page.once("dialog", handle_dialog)

        try:
            self.click(locator)
        except Exception as e:
            logging.error(f"Click failed: {e}")

    def assert_dialog_text(self, expected_text: str, accept: bool = False) -> None:
        """
        Asserts that a dialog appears and contains the expected text.
        If no dialog appears, logs an error.
        Args:
            expected_text (str): The text that should be present in the dialog.
            accept (bool): Set to True if you want to accept the dialog, by default is is set to False.
        """
        self._dialog_assertion_error = None

        def handle_dialog(dialog: Dialog, accept: bool = False):
            """
            Handles the dialog and asserts that the dialog contains the expected text.
            Args:
                dialog (Dialog): the playwright dialog object
                accept (bool): Set to True if you want to accept the dialog, by default is is set to False.
            """
            logging.info(f"Dialog appeared with message: {dialog.message}")
            actual_text = dialog.message
            try:
                assert (
                    expected_text in actual_text
                ), f"Expected dialog to contain '{expected_text}', but got '{actual_text}'"
            except AssertionError as e:
                self._dialog_assertion_error = e
            if accept:
                try:
                    dialog.accept()
                except Exception:
                    logging.warning("Dialog already accepted or handled")
            else:
                try:
                    dialog.dismiss()  # Dismiss dialog
                except Exception:
                    logging.warning("Dialog already dismissed or handled")

        self.page.once("dialog", lambda dialog: handle_dialog(dialog, accept))

    def go_to_log_in_page(self) -> None:
        """Click on the Log in button to navigate to the login page."""
        self.click(self.log_in_page)

    def safe_accept_dialog_select_option(self, locator: Locator, option: str) -> None:
        """
        Safely accepts a dialog triggered by selecting a dropdown, avoiding the error:
        playwright._impl._errors.Error: Dialog.accept: Cannot accept dialog which is already handled!
        If no dialog appears, continues without error.
        Args:
            locator (Locator): The locator that triggers the dialog when clicked.
            example: If clicking a save button opens a dialog, pass that save button's locator.
        """
        self.page.once("dialog", self._accept_dialog)
        try:
            locator.select_option(option)
        except Exception as e:
            logging.error(f"Option selection failed: {e}")
