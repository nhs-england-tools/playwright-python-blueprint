import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from pages.base_page import BasePage
from pages.alerts.alerts_page import AlertsPage
from pages.gfobt_test_kits.gfobt_test_kits_page import GFOBTTestKitsPage
from pages.screening_practitioner_appointments.screening_practitioner_appointments_page import (
    ScreeningPractitionerAppointmentsPage,
)
from pages.screening_subject_search.subject_screening_search_page import (
    SubjectScreeningPage,
)
from pages.surveillance.surveillance_summary_review_page import SurveillanceSummaryPage


# Scenario 1
@pytest.mark.regression
@pytest.mark.hub_user_tests
def test_hub_user_alerts_populated(page: Page) -> None:
    """
    Scenario: Hub User - Alerts populated
    This test ensures that the alerts have at least been populated for the user within a reasonable amount of time.
    """
    # Step 1: Log in as Hub Manager - State Registered (England)
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
    BasePage(page).click_refresh_alerts_link()

    # Step 2: Assert the refresh alerts button is visible
    alerts_page = AlertsPage(page)
    alerts_page.click_refresh_alerts()
    expect(alerts_page.refresh_alerts_link).to_be_visible(timeout=5000)


# Scenario 2
@pytest.mark.regression
@pytest.mark.hub_user_tests
def test_hub_user_kits_logged_not_read_report(page: Page) -> None:
    """
    Scenario: Hub User - Kits Logged Not Read report
    This test ensures that if available, the Kits Logged Not Read report loads within a reasonable amount of time.
    """
    # Step 1: Log in as Hub Manager - State Registered (England)
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
    BasePage(page).go_to_gfobt_test_kits_page()

    # Step 2: Assert the Kits Logged Not Read report loads as expected
    test_kits_page = GFOBTTestKitsPage(page)
    test_kits_page.open_test_kits_report()
    expect(test_kits_page.test_kits_header).to_be_visible(timeout=5000)


# Scenario 3
@pytest.mark.regression
@pytest.mark.hub_user_tests
def test_hub_user_people_requiring_colonoscopy_assessment_report(page: Page) -> None:
    """
    Scenario: Hub User - People Requiring Colonoscopy Assessment report
    This test ensures that if available, the People Requiring Colonoscopy Assessment report loads within a reasonable amount of time.
    """
    # Step 1: Log in as Hub Manager - State Registered (England)
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
    BasePage(page).go_to_screening_practitioner_appointments_page()

    # Step 2: Assert the People Requiring Colonoscopy Assessment report loads as expected
    appointments_page = ScreeningPractitionerAppointmentsPage(page)
    appointments_page.open_appointments_report()
    expect(appointments_page.appointments_header).to_be_visible(timeout=5000)


# Scenario 4
@pytest.mark.regression
@pytest.mark.hub_user_tests
def test_screening_centre_user_subject_search_and_summary(page: Page) -> None:
    """
    Scenario: Screening Centre User - Subject Search & Subject Summary
    This test ensures that the subject search works as expected and the subject summary loads and displays data correctly
    """
    # Step 1: Log in as Screening Centre Manager (England)
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()

    # Step 2: Use POM for subject search
    search_page = SubjectScreeningPage(page)
    """screening_status=4004 value represents 'Recall' & episode_status=2 value represents 'Closed'"""
    search_page.search_subject_with_args(
        surname="A*", forename="A*", screening_status="4004", episode_status="2"
    )


# Scenario 5
@pytest.mark.regression
@pytest.mark.hub_user_tests
def test_screening_centre_user_subject_search_and_surveillance(page: Page) -> None:
    """
    Scenario: Screening Centre User - Organisation Search & Surveillance Review Summary
    This test ensures that the organisation search works as expected and the surveillance review summary loads and displays data correctly
    """
    # Step 1: Log in as Screening Centre Manager (England)
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_organisations_page()

    # Step 2: Use POM for navigation and assertion
    sur_page = SurveillanceSummaryPage(page)
    sur_page.navigate_to_surveillance_review_summary()
    expect(sur_page.surveillance_review_summary_header).to_be_visible(timeout=5000)
