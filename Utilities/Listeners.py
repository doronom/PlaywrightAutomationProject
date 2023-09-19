# Import necessary modules and libraries.
import os
import pytest
from playwright.sync_api import sync_playwright


# Create a class called 'Listeners' for handling test-related actions.
class Listeners:
    def __init__(self):
        # Define a directory to store screenshots.
        self.screenshot_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)  # Create the screenshot directory
        self.page = None  # Store the Page instance

    # Define a pytest fixture to manage the browser instance.
    @pytest.fixture(scope="module", params=["chromium", "firefox", "webkit"])
    def browser(self, request):
        with sync_playwright() as p:
            browser_type = request.param
            browser = getattr(p, browser_type).launch(headless=False)
            yield browser
            browser.close()

    # Define a pytest fixture to manage the Page instance.
    @pytest.fixture(scope="function")
    def page(self, browser):
        page = browser.new_page()
        self.page = page  # Store the Page instance for later use
        yield page
        page.close()

    # Define a pytest fixture for taking a screenshot upon test failure.
    @pytest.fixture(scope="function", autouse=True)
    def screenshot_on_failure(self, request, page):
        yield
        if request.node.rep_call.failed:
            def take_screenshot():
                screenshot = self.page.screenshot()  # Use the stored Page instance
                screenshot_path = os.path.join(self.screenshot_dir, f"{request.node.name}.png")
                screenshot.save_as(screenshot_path)

            take_screenshot()

    # Define an on_finish method to clean up resources after all tests.
    def on_finish(self):
        if self.page:
            self.page.close()
        print("------------------- Tests Completed! Cleaning up... -------------------")

    # Define a pytest fixture for test setup.
    @pytest.fixture(scope="function", autouse=True)
    def test_listener(self, request):
        print("------------------- Test " + request.node.name + " is Starting! -------------------")

        def on_finish():
            print("------------------- Test " + request.node.name + " Completed! -------------------")

        request.addfinalizer(on_finish)

        request.node._testcase.instance = self  # Attach the Listeners instance to the instance
        yield self  # Yield the Listeners instance to the test function

        # Check if the test failed and take a screenshot if it did
        if request.node.rep_call.failed:
            def take_screenshot():
                screenshot = self.page.screenshot()  # Use the stored Page instance
                screenshot_dir = os.path.join(os.getcwd(), "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{request.node.name}.png")
                screenshot.save_as(screenshot_path)

            take_screenshot()

    # Define pytest fixtures for test setup, teardown, and failure handling.
    @pytest.fixture(scope="function", autouse=True)
    def handle_test_setup(self, request):
        def on_test_setup():
            print("Test Setup: " + request.node.name)
            # You can add custom setup logic here

        request.addfinalizer(on_test_setup)

    @pytest.fixture(scope="function", autouse=True)
    def handle_test_teardown(self, request):
        def on_test_teardown():
            print("Test Teardown: " + request.node.name)
            # You can add custom teardown logic here

        request.addfinalizer(on_test_teardown)

    @pytest.fixture(scope="function", autouse=True)
    def handle_test_failure(self, request):
        def on_test_failure():
            print("Test Failed: " + request.node.name)
            # You can add custom failure handling logic here

        request.addfinalizer(on_test_failure)
