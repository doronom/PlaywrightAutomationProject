from playwright.sync_api import Page, Locator

from Utilities.ProjectBase import ProjectBase


# The `MainPage` class is a representation of the main page of a web application
class MainPage(ProjectBase):
    def __init__(self, page):
        self.page = page

    # Property methods define locators for different elements on the web page.
    @property
    def next_page_button(self) -> Locator:
        return self.page.locator("svg[data-testid='ArrowRightIcon']")

    @property
    def back_page_button(self) -> Locator:
        return self.page.locator("svg[data-testid='ArrowLeftIcon']")

    @property
    def page_number_input(self) -> Locator:
        return self.page.locator("input[class='MuiInputBase-input MuiInput-input css-mnn31'][value]")

    @property
    def members_items(self) -> Locator:
        return self.page.locator("tr[class='MuiTableRow-root css-1gqug66']")

    @property
    def add_member_button(self) -> Locator:
        return self.page.locator("svg[data-testid='PersonAddIcon']")

    @property
    def first_name_input(self) -> Locator:
        return self.page.locator("(//input['MuiOutlinedInput-notchedOutline css-igs3ac'])[2]")

    @property
    def family_name_input(self) -> Locator:
        return self.page.locator("(//input['MuiOutlinedInput-notchedOutline css-igs3ac'])[3]")

    @property
    def add_button(self) -> Locator:
        return self.page.locator(
            "button.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")

    @property
    def table_row(self) -> Locator:
        return self.page.locator("//td['MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium css-q34dxg']")

    @property
    def table_all(self) -> Locator:
        return self.page.locator("table.MuiTable-root")

    # List of selector that required for the tests classes
    table_selector = "table.MuiTable-root"
    next_page_button_selector = "svg[data-testid='ArrowRightIcon']"
    back_page_button_selector = "svg[data-testid='ArrowLeftIcon']"
    members_items_selector = "tr[class='MuiTableRow-root css-1gqug66']"
    table_row_selector = "//td['MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium css-q34dxg']"

    # These are common interactions with web pages.

    def get_page_title(self) -> str:
        return self.page.title()

    def open_add_member_window(self):
        return self.add_member_button.click()

    def navigate_to_next_page(self):
        return self.next_page_button.click()

    def navigate_to_previous_page(self):
        return self.back_page_button.click()

    def fill_page_number_input(self, text: str):
        self.page_number_input.click()
        self.page_number_input.fill(text)

    def go_to_page_number_input(self):
        self.page_number_input.click()

    def fill_input_first_name(self, text: str):
        self.first_name_input.click()
        self.first_name_input.fill(text)

    def fill_input_family_name(self, text: str):
        self.family_name_input.click()
        self.family_name_input.fill(text)

    def add_new_member(self):
        return self.add_button.click()
