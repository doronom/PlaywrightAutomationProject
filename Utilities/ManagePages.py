# Import the 'Locators' module from 'PageObjects' for defining page locators.
import PageObjects as Locators

# Import the 'ProjectBase' base class from the 'Utilities' package.
from .ProjectBase import ProjectBase


# Create a class called 'ManagePages' that inherits from 'ProjectBase'.
class ManagePages(ProjectBase):
    # Static method 'init' to initialize the MainPage with the driver from 'ProjectBase'.
    @staticmethod
    def init():
        # Create an instance of the 'MainPage' using the driver from 'ProjectBase'.
        ProjectBase.MainPage = Locators.MainPage(ProjectBase.driver)
