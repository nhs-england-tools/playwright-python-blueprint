import logging
from playwright.sync_api import Page
from pages.monitoring_reports.sspi_update_warnings_base import (
    SSPIUpdateWarningsBasePage,
)


class SSPIUpdateWarningsInformationPage(SSPIUpdateWarningsBasePage):

    # Selectable Options

    HEADER = "SSPI Update Warnings - Information"
    AGE_OPTIONS = ["All", "Under 80", "80 and over"]
    REASONI_OPTIONS = ["Removal", "Subject joined BSO", "Subject left BSO"]
    WARNINGI_OPTIONS = [
        "Adoption",
        "Armed Services",
        "Embarkation",
        "Mental Hospital",
        "No open episodes",
        "No open or changed episodes",
        "Not provided",
        "Other reason",
        "Previous end code changed",
        "Removal",
        "Service dependent",
    ]
    TABLE_ID = "#sspiUpdateWarningList"
    TABLE_FIRST_ROW = f"{TABLE_ID} > tbody > tr:nth-child(1)"
    TABLE_FIRST_NHS_NUMBER = f"{TABLE_FIRST_ROW} > td:nth-child(3)"
    TABLE_FIRST_FAMILY_NAME = f"{TABLE_FIRST_ROW} > td:nth-child(4)"
    TABLE_FIRST_FIRST_NAME = f"{TABLE_FIRST_ROW} > td:nth-child(5)"

    def __init__(self, page: Page) -> None:
        SSPIUpdateWarningsBasePage.__init__(self, page)
        self.HEADER = "SSPI Update Warnings - Information"
        self.API_REQUEST = "**/bss/report/sspiUpdateWarnings/information/search**"
