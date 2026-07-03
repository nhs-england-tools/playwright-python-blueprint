"""
This file contains tests that save clinical content and then checks the history log.
"""

import pytest
import os
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.questions.edit_question_page import EditQuestionPage
from pages.questions.search_questions_page import SearchQuestionsPage
from pages.care_advice.edit_care_advice_page import EditCareAdvicePage
from pages.care_advice.search_care_advice_page import SearchCareAdvicePage
from pages.dispositions.edit_disposition_page import EditDispositionPage
from pages.dispositions.search_dispositions_page import SearchDispositionsPage
from pages.pathways.edit_pathway_page import EditPathwayPage
from pages.pathways.search_pathways_page import SearchPathwaysPage
from pages.paccs.templates.edit_template_page import EditTemplatePage
from pages.paccs.templates.search_templates_page import SearchTemplatesPage
from pages.paccs.conditions.edit_condition_page import EditConditionPage
from pages.paccs.conditions.search_conditions_page import SearchConditionsPage
from pages.misc.symptom_group.edit_symptom_group_page import EditSymptomGroupPage
from pages.misc.symptom_group.search_symptom_groups_page import SearchSymptomGroupsPage
from pages.misc.symptom_discriminator.edit_symptom_discriminator_page import (
    EditSymptomDiscriminatorPage,
)
from pages.misc.symptom_discriminator.search_symptom_discriminators_page import (
    SearchSymptomDiscriminatorsPage,
)

VERSION_NUMBER = "42.2.0"
AUTHOR_NOTE = "Regression testing"


@pytest.fixture(autouse=True)
def login(page: Page) -> None:
    page.goto("/")
    page.get_by_role("button", name="Allow all cookies").click()
    page.get_by_placeholder("Email address").fill(
        "nhspathways.test+pwteammember@nhs.net"
    )
    page.get_by_placeholder("Password").fill(os.getenv("USER_PASS"))
    page.get_by_role("button", name="Sign in", exact=True).click()


def test_save_question(page: Page) -> None:
    """
    This test saves a question against a previous release and checks history log to confirm correct release
    """
    HomePage(page).navigate_to_search_questions()
    SearchQuestionsPage(page).search_by_question_id("Tx226532")
    page.wait_for_timeout(2000) #wait for now but needs logic to wait for the page to load fully
    EditQuestionPage(page).save_clinical_content(VERSION_NUMBER, AUTHOR_NOTE, "questions")
    EditQuestionPage(page).click_change_history_log()

    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(AUTHOR_NOTE)
    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(f"Target {VERSION_NUMBER}(0)")



def test_save_care_advice(page: Page) -> None:
    """
    This test saves care advice against a previous release and checks history log to confirm correct release
    """
    HomePage(page).navigate_to_search_care_advice()
    SearchCareAdvicePage(page).search_by_care_advice_id("Cx221784")
    page.wait_for_timeout(2000)
    EditCareAdvicePage(page).save_clinical_content(VERSION_NUMBER, AUTHOR_NOTE)
    EditCareAdvicePage(page).click_change_history_log()

    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(AUTHOR_NOTE)
    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(f"Target {VERSION_NUMBER}(0)")



def test_save_disposition(page: Page) -> None:
    """
    This test saves a disposition against a previous release and checks history log to confirm correct release
    """
    HomePage(page).navigate_to_search_dispositions()
    SearchDispositionsPage(page).search_by_disposition_id("Dx220235")
    page.wait_for_timeout(2000)
    EditDispositionPage(page).save_clinical_content(VERSION_NUMBER, AUTHOR_NOTE)
    EditDispositionPage(page).click_change_history_log()

    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(AUTHOR_NOTE)
    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(f"Target {VERSION_NUMBER}(0)")



def test_save_pathway(page: Page) -> None:
    """
    This test saves a pathway against a previous release and checks history log to confirm correct release
    """
    HomePage(page).navigate_to_search_pathways()
    SearchPathwaysPage(page).search_by_pathway_id("PW1899")
    page.wait_for_timeout(2000)
    EditPathwayPage(page).save_clinical_content(VERSION_NUMBER, AUTHOR_NOTE)
    EditPathwayPage(page).click_change_history_log()

    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(AUTHOR_NOTE)
    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(f"Target {VERSION_NUMBER}(0)")


def test_save_template(page: Page) -> None:
    """
    This test saves a template against a previous release and checks history log to confirm correct release
    """
    HomePage(page).navigate_to_search_templates()
    SearchTemplatesPage(page).search_by_template_id("Cs000138")
    page.wait_for_timeout(2000)
    EditTemplatePage(page).save_clinical_content(VERSION_NUMBER, AUTHOR_NOTE)
    EditTemplatePage(page).click_change_history_log()

    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(AUTHOR_NOTE)
    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(f"Target {VERSION_NUMBER}(0)")


def test_save_condition(page: Page) -> None:
    """
    This test saves a condition against a previous release and checks history log to confirm correct release
    """
    HomePage(page).navigate_to_search_conditions()
    SearchConditionsPage(page).search_by_condition_id("Cn010727")
    page.wait_for_timeout(2000)
    EditConditionPage(page).save_clinical_content(VERSION_NUMBER, AUTHOR_NOTE, "conditions")
    EditConditionPage(page).click_change_history_log()

    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(AUTHOR_NOTE)
    expect(page.get_by_label("History/Notes").locator("tbody")).to_contain_text(f"Target {VERSION_NUMBER}(0)")



def test_save_symptom_group(page: Page) -> None:
    """
    This test saves a symptom group against a previous release and checks history log to confirm correct release
    """
    HomePage(page).navigate_to_search_symptom_groups()
    SearchSymptomGroupsPage(page).search_by_symptom_group_id("SG1272")
    page.wait_for_timeout(2000)
    EditSymptomGroupPage(page).save_clinical_content(VERSION_NUMBER, AUTHOR_NOTE)
    EditSymptomGroupPage(page).click_change_history_log()

    expect(page.locator("#tableExpandCollapse")).to_contain_text(AUTHOR_NOTE)
    expect(page.locator("#tableExpandCollapse")).to_contain_text(f"Target {VERSION_NUMBER}(0)")



def test_save_symptom_discriminator(page: Page) -> None:
    """
    This test saves a symptom discriminator against a previous release and checks history log to confirm correct release
    """
    HomePage(page).navigate_to_search_symptom_discriminators()
    SearchSymptomDiscriminatorsPage(page).search_by_symptom_discriminator_id("SD4785")
    page.wait_for_timeout(2000)
    EditSymptomDiscriminatorPage(page).save_clinical_content(VERSION_NUMBER, AUTHOR_NOTE)
    EditSymptomDiscriminatorPage(page).click_change_history_log()

    expect(page.locator("#tableExpandCollapse")).to_contain_text(AUTHOR_NOTE)
    expect(page.locator("#tableExpandCollapse")).to_contain_text(f"Target {VERSION_NUMBER}(0)")
