# tests/test_member_display_per_page.py

import pytest
from Configuration.Configuration import URL
from PageObjects.MainPage import MainPage
from Utilities.Listeners import Listeners
from conftest import browser, page # Import fixtures from CommonOps module

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


class TestMembersDisplayPerPage:

    def test_members_display_per_page(self, setup, page):
        main_page = setup
        # Wait for the member items to load
        page.wait_for_selector(main_page.members_items_selector, timeout=5000)

        # Count the number of displayed member items on the page
        member_elements = page.query_selector_all(main_page.members_items_selector)
        num_of_members = len(member_elements)
        assert num_of_members == 10, f"Expected 10 members per page, but found {num_of_members}."
