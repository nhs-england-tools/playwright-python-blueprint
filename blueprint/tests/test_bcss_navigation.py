import pytest
from playwright.sync_api import Page, expect

@pytest.mark.skip
def bcss_login(page: Page) -> None:
    page.goto('https://bcss-test-ddc-bcss.k8s-nonprod.texasplatform.uk/')
    page.get_by_placeholder("Username").fill("BCSS401")
    page.get_by_placeholder("Password").fill("changeme")
    page.get_by_role("button", name="signInSubmitButton").click()
