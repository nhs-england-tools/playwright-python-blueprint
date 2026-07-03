"""
This file contains tests for uploading files to PAT enquiries. It tests that different file types can be uploaded and deleted successfully.
"""

import pytest
import os
from playwright.sync_api import Page, expect
from pytest_playwright.pytest_playwright import page


@pytest.mark.parametrize(
    "file_to_test", ["regression_test_document.docx", "regression_test_document.pdf"]
)
def test_file_type_upload_to_enquiry(page: Page, file_to_test: str) -> None:
    """
    This test confirms different file types can be uploaded to an enquiry.
    File used for this test: {file_to_test}
    """
    page.goto("/")
    page.get_by_role("button", name="Allow all cookies").click()
    page.get_by_placeholder("Email address").fill(
        "nhspathways.test+pwteammember@nhs.net"
    )
    page.get_by_placeholder("Password").fill(os.getenv("USER_PASS"))
    page.get_by_role("button", name="Sign in").click()
    page.get_by_role("button", name="Enquiries").click()
    page.get_by_title("Search all clinical enquiries").click()
    page.get_by_label("Enquiry ID").fill("FUDMB39086")
    page.get_by_role("button", name=" Search").click()
    page.get_by_role("link", name="FUDMB39086").click()

    with page.expect_file_chooser() as fc_info:
        page.locator("#txtUploadFile1").click()
        file_chooser = fc_info.value
        file_chooser.set_files(f"{os.getcwd()}/tests/resources/{file_to_test}")
    page.get_by_role("button", name="Upload").click()
    expect(page.get_by_role("cell", name=f"{file_to_test}")).to_be_visible()

    page.wait_for_load_state("networkidle")  # ensures JS is fully initialised
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_title("Delete attachment", exact=True).click()

    expect(page.locator("#remove-attachment-feedback")).to_contain_text("xAttachment successfully deleted")
