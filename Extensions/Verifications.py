# extensions/Verifications.py

from PageObjects.MainPage import MainPage
from playwright.sync_api import Page


class Verifications:
    def __init__(self, page: Page):
        self.page = page

    def validate_members_per_page(self, page_number: int):
        main_page = MainPage(self.page)
        # Wait for the member items to load
        self.page.wait_for_selector(main_page.members_items_selector, timeout=5000)
        member_elements = self.page.query_selector_all(main_page.members_items_selector)
        # Check if all columns display the error message "Data can't be processed"
        all_errors = all(element.inner_text() == "Data can't be processed" for element in member_elements)

        # Check if all columns display "null"
        all_null = all(element.inner_text() == "null" for element in member_elements)

        if all_errors or all_null:
            num_of_members = 0
        else:
            num_of_members = len(member_elements)
        assert num_of_members == 10, f"Expected 10 members per page on page {page_number}, but found {num_of_members}."
