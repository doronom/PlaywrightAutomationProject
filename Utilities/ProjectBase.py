from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, BrowserContext


class ProjectBase:
    driver: Page = None
    MainPage = None

    def __init__(self, page: Page):
        self.page = page

    def is_title_contains(self, text):
        title = self.page.title()
        if title.find(text) == -1:
            return False
        else:
            return True

    def is_url_contains(self, text):
        if self.page.url.find(text) == -1:
            return False
        else:
            return True

    @staticmethod
    def initialize_playwright():
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            ProjectBase.driver = context.new_page()

    @staticmethod
    def close_playwright():
        if ProjectBase.driver:
            ProjectBase.driver.context().close()
            ProjectBase.driver = None
