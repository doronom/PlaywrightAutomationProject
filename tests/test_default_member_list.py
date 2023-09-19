# tests/test_default_member_list.py

import pytest
from Configuration.Configuration import URL
from conftest import browser, page
from Extensions.Verifications import Verifications
from PageObjects.MainPage import MainPage
from Utilities.Listeners import Listeners

# Define a global variable to store the Listeners instance
listeners = None


@pytest.fixture(scope="module", autouse=True)
def setup_listeners():
    global listeners
    listeners = Listeners()


@pytest.fixture(autouse=True)
def event_listener(request):
    yield
    if listeners:
        listeners.on_finish()


@pytest.fixture
def setup(browser, page):
    main_page = MainPage(page)
    page.goto(URL)
    yield main_page
    page.close()


class TestDefaultMemberList:

    def test_default_member_list(self, setup, page):
        main_page = setup
        # Wait for the member list to load
        page.wait_for_selector(main_page.table_selector, timeout=5000)
        # Check if the member list is displayed on the first page
        is_member_list_displayed = page.is_visible(main_page.table_selector)
        assert is_member_list_displayed, "Default member list is not displayed on the first page."

