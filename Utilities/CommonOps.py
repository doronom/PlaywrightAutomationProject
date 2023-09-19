# /Utilities/CommonOps.py

import pytest
from playwright.sync_api import sync_playwright


# Define a fixture for browser setup
@pytest.fixture(scope="module", params=["chromium", "firefox", "webkit"])
def browser(request):
    with sync_playwright() as p:
        browser_type = request.param
        browser = getattr(p, browser_type).launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="module")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
