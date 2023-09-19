from playwright.sync_api import Page, BrowserContext

import PageObjects as Locators
from .ProjectBase import ProjectBase  # Import Base class from the Utilities package


class ManagePages(ProjectBase):
    @staticmethod
    def init():
        ProjectBase.MainPage = Locators.MainPage(ProjectBase.driver)
