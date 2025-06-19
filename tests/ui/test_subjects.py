"""
Subjects Tests: These tests cover viewing subjects via Subject Search.
"""

import pytest
from secrets import randbelow
from pages.main_menu import MainMenuPage
from utils.user_tools import UserTools
from utils.nhs_number_tools import NHSNumberTools
from playwright.sync_api import Page, expect

# Fixtures


@pytest.fixture(autouse=True)
def log_in(user_tools: UserTools, page: Page) -> None:
    user_tools.user_login(page, "BSO User - BS1")
    MainMenuPage(page).select_menu_option("Subject Search")


# Tests


@pytest.mark.subjects
def test_subject_search(page: Page) -> None:
    """
    Navigate to subject search, search for a subject family name starting with the letter A, select a random result and
    confirm the correct Subject Details page is loaded.
    """
    # Wait for the JSON database request to complete and search on letter A
    with page.expect_response("**/bss/subjects/search**") as response:
        # Await initial API load, but don't need to do anything with response at this stage
        pass
    page.locator("#familyNameFilter").get_by_role("textbox").fill("A")

    # Wait for the JSON database request to complete, select a random result from the JSON and select
    with page.expect_response("**/bss/subjects/search**") as response:
        selected_number = randbelow(len(response.value.json()["results"]))
        nhs_number = NHSNumberTools().spaced_nhs_number(
            response.value.json()["results"][selected_number]["nhsNumber"]
        )
    page.get_by_text(nhs_number).dblclick()

    # Show subject details and confirm correct page is present
    expect(page.get_by_text("Subject Details")).to_be_visible()
    expect(page.get_by_text(nhs_number)).to_be_visible()
