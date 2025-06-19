import pytest
from utils.user_tools import UserTools
from playwright.sync_api import Playwright, BrowserContext


def persist_browser_context(playwright: Playwright, base_url: str) -> BrowserContext:
    return playwright.chromium.launch_persistent_context("", base_url=base_url)


@pytest.fixture(scope="session")
def api_bso_user_session(
    user_tools: UserTools, playwright: Playwright, base_url: str
) -> BrowserContext:
    context = persist_browser_context(playwright, base_url)
    user_tools.user_login(context.new_page(), "BSO User - BS1")
    return context


@pytest.fixture(scope="session")
def api_national_user_session(
    user_tools: UserTools, playwright: Playwright, base_url: str
) -> BrowserContext:
    context = persist_browser_context(playwright, base_url)
    user_tools.user_login(context.new_page(), "National User")
    return context


@pytest.fixture(scope="session")
def api_helpdesk_session(
    user_tools: UserTools, playwright: Playwright, base_url: str
) -> BrowserContext:
    context = persist_browser_context(playwright, base_url)
    user_tools.user_login(context.new_page(), "Helpdesk User")
    return context
