# tests/test_add_new_member.py

import pytest
from Configuration.Configuration import URL
from PageObjects.MainPage import MainPage
from conftest import browser, page  # Import fixtures from CommonOps module
from Utilities.Listeners import Listeners

# Define a global variable to store the Listeners instance
listeners = None
last_page = "16"

# Define a list of test data with multiple first names and family names
test_data = [
    ("New Member First Name", "New Member Family Name"),  # legal data
    ('', ''),  # illegal input - empty fields
    ("First&^%*() Name 2", "Family890!@# Name 2"),  # illegal input - numbers and symbols
    ("S", "G"),  # illegal input - below min length
    ("Test a long string in the first name field ABCDEFGHIGKLMNOPQRSTUVWXYZ",
     "Test a long string in the first name field "
     "ABCDEFGHIGKLMNOPQRSTUVWXYZ")  # illegal input - above max length

]


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


class TestAddNewMember:

    @pytest.mark.parametrize("first_name, last_name", test_data)
    def test_add_new_member(self, setup, page, first_name, last_name):
        main_page = setup
        # Click the "Add Member" button to open the add member form
        main_page.open_add_member_window()

        # Fill in the member details (firstName and familyName)
        main_page.fill_input_first_name(first_name)
        main_page.fill_input_family_name(last_name)

        # Click the "Add" button to add the new member
        main_page.add_new_member()

        # Skip to page 11 where the new member should be displayed:
        main_page.go_to_page_number_input()
        page.keyboard.press("Backspace")
        main_page.fill_page_number_input(last_page)
        page.keyboard.press("Enter")
        page.wait_for_selector(main_page.back_page_button_selector, timeout=5000)

        # Wait for the table rows to load
        page.wait_for_selector(main_page.members_items_selector, timeout=10000)

        # Find the newly added member in the table and validate the text
        rows = page.query_selector_all(main_page.table_row_selector)
        found = False

        for row in rows:
            columns = row.query_selector_all("td")  # Locate all <td> elements within the row
            if len(columns) >= 3:  # Ensure there are at least 3 columns (ID, Name, Family)
                f_name = columns[1].inner_text()  # Get the text of the second column (Name)
                l_name = columns[2].inner_text()  # Get the text of the third column (Family)

                if f_name == first_name and l_name == last_name:
                    found = True
                    break

        assert found, f"Newly added member ({first_name}, {last_name}) not found in the table."
