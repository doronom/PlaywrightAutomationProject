# ./conftest.py

import pytest
from playwright.sync_api import sync_playwright, Playwright, BrowserContext
from Configuration.Configuration import URL
from PageObjects.MainPage import MainPage
from Utilities.Listeners import Listeners


listeners = None


@pytest.fixture(scope="session", autouse=True)
def playwright() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


# Define a parameterized fixture for browser setup
@pytest.fixture(scope="module", params=["chromium", "firefox", "webkit"])
def browser(request):
    with sync_playwright() as p:
        browser_type = request.param
        browser = getattr(p, browser_type).launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(autouse=True)
def setup_listener(request):
    global listeners
    listeners = Listeners()
    yield listeners
    listeners.on_finish()


@pytest.fixture
def setup(browser, page, autouse=True):
    main_page = MainPage(page)
    page.goto(URL)
    yield main_page
    page.close()
