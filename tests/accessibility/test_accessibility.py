"""
Accessibility Tests: This covers accessibility scanning using axe-core for each url in the LIST_OF_PAGES.
"""

import pytest
from playwright.sync_api import Page
from utils.axe import Axe
from utils.user_tools import UserTools


LIST_OF_PAGES = [
    "home",
    # Subjects
    "subjects",
    "subjects/9300000001",
    # Batch Management
    "batch/list",
    "fsBatch/create",
    "rispAgexBatch/create",
    "ntddBatch/create",
    # Outcome List
    "outcome/list",
    # Parameters
    "gpPracticeGroup/list",
    "gpPracticeGroup/create",
    "outcodeGroup/list",
    "outcodeGroup/create",
    "rispDefaults",
    "bsoDefaults",
    "failsafeParameters",
    # BSO Mapping
    "gpPractice/list",
    "gpPractice/A12345",
    "assignedGpPractice/list",
    "outcode/list",
    "outcodeView/EX1",
    # BSO Contact List
    "bso/list",
    "bso/AGA",
]


@pytest.mark.specific_requirement
@pytest.mark.accessibility
def test_accessibility_sweep(page: Page, user_tools: UserTools) -> None:
    """This test will loop through each page on the list of pages, and run Axe to generate an accessibility report."""

    user_tools.user_login(page, "BSO User - BS1")

    for url in LIST_OF_PAGES:
        page.goto(f"/bss/{url}")
        Axe.run(page, filename=url.replace("/", "__"))
