"""
Smoke Tests: These are the smoke tests for the BS-Select pipeline.
"""

import pytest
from pages.main_menu import MainMenuPage
from utils.user_tools import UserTools
from playwright.sync_api import Page, expect


pytestmark = [pytest.mark.smoke]

# Fixtures


@pytest.fixture(autouse=True)
def log_in(user_tools: UserTools, page: Page) -> None:
    user_tools.user_login(page, "BSO User - BS1")


# Tests


def test_subject_search(page: Page) -> None:
    """
    From the main menu, navigate to Subject Search and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option("Subject Search")
    expect(page.get_by_role("heading")).to_contain_text("Subject Search")


def test_batch_list(page: Page) -> None:
    """
    From the main menu, navigate to Batch Management -> Batch List and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    expect(page.get_by_role("heading")).to_contain_text("Batch List")


def test_outcome_list(page: Page) -> None:
    """
    From the main menu, navigate to Outcome List and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option("Outcome List")
    expect(page.get_by_role("heading")).to_contain_text("Outcome List")


def test_parameters(page: Page) -> None:
    """
    From the main menu, navigate to Parameters -> Monthly Failsafe Report and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option("Parameters", "Monthly Failsafe Report")
    expect(page.get_by_role("heading")).to_contain_text(
        "Monthly Failsafe Report Parameters"
    )


def test_bso_mapping(page: Page) -> None:
    """
    From the main menu, navigate to BSO Mapping -> GP Practice List and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option("BSO Mapping", "GP Practice List")
    expect(page.get_by_role("heading")).to_contain_text("GP Practice List")


def test_bso_contact_list(page: Page) -> None:
    """
    From the main menu, navigate to BSO Contact List and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option("BSO Contact List")
    expect(page.get_by_role("heading")).to_contain_text("BSO Contact List")


def test_monitoring_reports(page: Page) -> None:
    """
    From the main menu, navigate to Monitoring Reports -> SSPI Update Warnings and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option(
        "Monitoring Reports", "SSPI Update Warnings - Action"
    )
    expect(page.get_by_role("heading")).to_contain_text("SSPI Update Warnings - Action")


def test_failsafe_reports(page: Page) -> None:
    """
    From the main menu, navigate to Failsafe Reports -> Batch Analysis Report List and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option(
        "Failsafe Reports", "Batch Analysis Report List"
    )
    expect(page.get_by_role("heading")).to_contain_text("Batch Analysis Report List")


def test_estimating(page: Page) -> None:
    """
    From the main menu, navigate to Estimating -> NTDD Screening Estimate List and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option("Estimating", "NTDD Screening Estimate List")
    expect(page.get_by_role("heading")).to_contain_text("NTDD Screening Estimate List")


def test_round_planning(page: Page) -> None:
    """
    From the main menu, navigate to Round Planning -> Current and Next Visit List and confirm the header has rendered correctly.
    """
    MainMenuPage(page).select_menu_option(
        "Round Planning", "Current and Next Visit List"
    )
    expect(page.get_by_role("heading")).to_contain_text("Current and next visits")
