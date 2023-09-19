# Import necessary modules from Playwright library.
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page


# Create a base class for a project.
class ProjectBase:
    # Initialize class variables for driver and MainPage.
    driver: Page = None
    MainPage = None

    # Constructor to initialize the object with a Page.
    def __init__(self, page: Page):
        self.page = page

    # Method to check if the page title contains a specific text.
    def is_title_contains(self, text):
        title = self.page.title()
        if title.find(text) == -1:
            return False
        else:
            return True

    # Method to check if the page URL contains a specific text.
    def is_url_contains(self, text):
        if self.page.url.find(text) == -1:
            return False
        else:
            return True

    # Static method to initialize Playwright for browser automation.
    @staticmethod
    def initialize_playwright():
        # Use a context manager to work with Playwright.
        with sync_playwright() as p:
            # Launch a Chromium browser.
            browser = p.chromium.launch()
            # Create a new browser context.
            context = browser.new_context()
            # Create a new Page instance and assign it to the class variable driver.
            ProjectBase.driver = context.new_page()

    # Static method to close Playwright resources.
    @staticmethod
    def close_playwright():
        if ProjectBase.driver:
            # Close the context associated with the driver.
            ProjectBase.driver.context().close()
            # Set the driver to None to release resources.
            ProjectBase.driver = None
