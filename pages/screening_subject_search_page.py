from playwright.sync_api import Page


class ScreeningStatusSearchOptions:
    def __init__(self, page: Page):
        self.page = page

        # Locate screening status dropdown list
        self.select_status = self.page.locator("#A_C_ScreeningStatus")

    # Select screening status options
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


class LatestEpisodeStatusSearchOptions:
    def __init__(self, page: Page):
        self.page = page

        # Locate latest episode status status dropdown list
        self.select_status = self.page.locator("#A_C_EpisodeStatus")

    # Select latest episode status options
    def select_status_open_paused(self):
        self.select_status.select_option("1")

    def select_status_closed(self):
        self.select_status.select_option("2")

    def select_status_no_episode(self):
        self.select_status.select_option("3")


class SearchAreaSearchOptions:
    def __init__(self, page: Page):
        self.page = page

        # Locate search area dropdown list
        self.select_area = self.page.locator("#A_C_SEARCH_DOMAIN")

    # Select search area options
    def select_search_area_home_hub(self):
        self.select_area.select_option("01")

    def select_search_area_gp_practice(self):
        self.select_area.select_option("02")

    def select_search_area_ccg(self):
        self.select_area.select_option("03")

    def select_search_area_screening_centre(self):
        self.select_area.select_option("05")

    def select_search_area_other_hub(self):
        self.select_area.select_option("06")

    def select_search_area_whole_database(self):
        self.select_area.select_option("07")
