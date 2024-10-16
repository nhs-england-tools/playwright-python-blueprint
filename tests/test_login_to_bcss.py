import pytest
from playwright.sync_api import Page, expect

@pytest.mark.example
def test_login_to_bcss(page: Page) -> None:

    # Navigate to page
    page.goto("https://bcss-test-ddc-bcss.k8s-nonprod.texasplatform.uk/")

    # Enter username and password and click sign in button
    page.get_by_role("textbox", name="Username").fill("BCSS401")
    page.get_by_role("textbox", name="Password").fill("changeme")
    page.get_by_role("button", name="submit").click()

    # # Assert the page loaded is the bcss dashboard (the only available locator was CSS path)
    expect(page.locator
           ("html body table.masterTable tbody tr td table.PageDefault tbody tr td table tbody tr td font.pageTitle span#ntshAppTitle")
           ).to_contain_text("Bowel Cancer Screening System")
