# tests/TestPagination.py

import pytest
from Configuration.Configuration import URL
from conftest import browser, page
from Extensions.Verifications import Verifications
from PageObjects.MainPage import MainPage
from Utilities.Listeners import Listeners

# Define a global variable to store the Listeners instance
listeners = None
last_page = "10"


# Fixture to set up the Listeners instance before any tests in this module run.
@pytest.fixture(scope="module", autouse=True)
def setup_listeners():
    global listeners
    listeners = Listeners()


# Fixture to handle events during test execution, like cleanup.
@pytest.fixture(autouse=True)
def event_listener(request):
    yield
    if listeners:
        listeners.on_finish()


# Fixture to set up the test environment with the main page and verifications.
@pytest.fixture
def setup(browser, page):
    main_page = MainPage(page)
    verifications = Verifications(page)
    page.goto(URL)
    yield main_page, verifications
    page.close()


class TestPagination:
    # Test method to validate forward pagination using the right arrow button.
    @pytest.mark.sanity
    def test_fw_pagination_using_right_arrow_button(self, setup, page):
        main_page, verifications = setup
        # Wait for the pagination elements to load
        page.wait_for_selector(main_page.next_page_button_selector, timeout=5000)
        for page_number in range(1, 11):
            # Click the next page button
            main_page.navigate_to_next_page()
            verifications.validate_members_per_page(page_number + 1)

    # Test method to validate backward pagination using the left arrow button.
    @pytest.mark.sanity
    def test_backward_pagination_using_left_arrow_button(self, setup, page):
        main_page, verifications = setup
        # Skip to the page 10 (the last page):
        main_page.go_to_page_number_input()
        page.keyboard.press("Backspace")
        main_page.fill_page_number_input(last_page)
        page.keyboard.press("Enter")
        # Wait for the table rows to load and the back arrow button to be clickable
        page.wait_for_selector(main_page.members_items_selector, timeout=10000)
        page.wait_for_selector(main_page.back_page_button_selector, timeout=5000)
        for page_number in range(10, 1, -1):
            main_page.navigate_to_previous_page()
            page.wait_for_selector(main_page.members_items_selector, timeout=10000)
            verifications.validate_members_per_page(page_number - 1)

    # Test method to validate pagination using the input field.
    @pytest.mark.sanity
    def test_pagination_using_input(self, setup, page):
        main_page, verifications = setup
        for page_number in range(1, 11):
            main_page.go_to_page_number_input()
            # Clear any existing text in the input field
            page.keyboard.press("Backspace")
            main_page.fill_page_number_input(str(page_number))
            page.keyboard.press("Enter")
            page.wait_for_selector(main_page.members_items_selector, timeout=5000)
            verifications.validate_members_per_page(page_number)
