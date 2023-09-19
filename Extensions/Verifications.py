# extensions/Verifications.py

from PageObjects.MainPage import MainPage
from playwright.sync_api import Page


# Create a class called 'Verifications' for handling verification actions.
class Verifications:
    def __init__(self, page: Page):
        self.page = page

    # Define a method for validating the number of members per page.
    def validate_members_per_page(self, page_number: int):
        main_page = MainPage(self.page)
        # Wait for the member items to load using the selector from the MainPage class.
        self.page.wait_for_selector(main_page.members_items_selector, timeout=5000)
        # Query all member elements on the page using the selector from the MainPage class.
        member_elements = self.page.query_selector_all(main_page.members_items_selector)
        if len(member_elements) == 1:
            num_of_members = 0
        else:
            num_of_members = len(member_elements)

        # Check if all columns display the error message "Data can't be processed."
        all_errors = all(element.inner_text() == "Data can't be processed" for element in member_elements)

        # Check if all columns display "null."
        all_null = all(element.inner_text() == "null" for element in member_elements)

        # In case of error was found return no members found.
        if all_errors or all_null:
            num_of_members = 0

        # Assert that the number of members matches the expected count (10 members per page).
        assert num_of_members == 10, f"Expected 10 members per page on page {page_number}, but found {num_of_members}."
