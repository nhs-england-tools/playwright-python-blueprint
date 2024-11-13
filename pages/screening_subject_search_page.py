from playwright.sync_api import Page


class ScreeningSubjectPage:
    def __init__(self, page: Page):
        self.page = page

        self.select_status = self.page.locator("#A_C_ScreeningStatus")

    def select_status_call(self):
        self.select_status.select_option("4001")

    def select_status_inactive(self):
        self.select_status.select_option("4002")

    def select_status_recall(self):
        self.select_status.select_option("4004")

    def select_status_opt_in(self):
        self.select_status.select_option("4003")

    def select_status_self_referral(self):
        self.select_status.select_option("4005")

    def select_status_surveillance(self):
        self.select_status.select_option("4006")

    def select_status_seeking_further_data(self):
        self.select_status.select_option("4007")

    def select_status_ceased(self):
        self.select_status.select_option("4008")

    def select_status_bowel_scope(self):
        self.select_status.select_option("4009")

    def select_status_lynch_surveillance(self):
        self.select_status.select_option("306442")

    def select_status_lynch_self_referral(self):
        self.select_status.select_option("307129")
