from playwright.sync_api import Page


class BcssHomePage:
    def __init__(self, page: Page):
        self.page = page
        # Homepage links
        self.sub_menu_link = self.page.get_by_role("link", name="Show Sub-menu")
        self.hide_sub_menu_link = self.page.get_by_role("link", name="Hide Sub-menu")
        self.select_org_link = self.page.get_by_role("link", name="Select Org")
        self.back_button = self.page.get_by_role("link", name="Back")
        self.release_notes_link = self.page.get_by_role("link", name="- Release Notes")
        self.refresh_alerts_link = self.page.get_by_role("link", name="Refresh alerts")
        self.user_guide_link = self.page.get_by_role("link", name="User guide")
        self.help_link = self.page.get_by_role("link", name="Help")

    def click_sub_menu_link(self):
        self.sub_menu_link.click()

    def click_hide_sub_menu_link(self):
        self.hide_sub_menu_link.click()

    def click_select_org_link(self):
        self.select_org_link.click()

    def click_back_button(self):
        self.back_button.click()

    def click_release_notes_link(self):
        self.release_notes_link.click()

    def click_refresh_alerts_link(self):
        self.refresh_alerts_link.click()

    def click_user_guide_link(self):
        self.user_guide_link.click()

    def click_help_link(self):
        self.help_link.click()


class MainMenu:
    def __init__(self, page: Page):
        self.page = page
        # Main menu - page links
        self.contacts_list_page = self.page.get_by_role("link", name="Contacts List")
        self.bowel_scope_page = self.page.get_by_role("link", name="Bowel Scope")
        self.call_and_recall_page = self.page.get_by_role("link", name="Call and Recall")
        self.communications_production_page = self.page.get_by_role("link", name="Communications Production")
        self.download_page = self.page.get_by_role("link", name="Download")
        self.fit_test_kits_page = self.page.get_by_role("link", name="FIT Test Kits")
        self.gfob_test_kits_page = self.page.get_by_role("link", name="gFOBT Test Kits")
        self.lynch_surveillance_page = self.page.get_by_role("link", name="Lynch Surveillance")
        self.organisations_page = self.page.get_by_role("link", name="Organisations")
        self.reports_page = self.page.get_by_role("link", name="Reports")
        self.screening_practitioner_appointments_page = self.page.get_by_role("link", name="Screening Practitioner")
        self.screening_subject_search_page = self.page.get_by_role("link", name="Screening Subject Search")

    def go_to_contacts_list_page(self):
        self.contacts_list_page.click()

    def go_to_bowel_scope_page(self):
        self.bowel_scope_page.click()

    def go_to_call_and_recall_page(self):
        self.call_and_recall_page.click()

    def go_to_communications_production_page(self):
        self.communications_production_page.click()

    def go_to_download_page(self):
        self.download_page.click()

    def go_to_fit_test_kits_page(self):
        self.fit_test_kits_page.click()

    def go_to_gfob_test_kits_page(self):
        self.gfob_test_kits_page.click()

    def go_to_lynch_surveillance_page(self):
        self.lynch_surveillance_page.click()

    def go_to_organisations_page(self):
        self.organisations_page.click()

    def go_to_reports_page(self):
        self.reports_page.click()

    def go_to_screening_practitioner_appointments_page(self):
        self.screening_practitioner_appointments_page.click()

    def go_to_screening_subject_search_page(self):
        self.screening_subject_search_page.click()
