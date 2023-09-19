# tests/test_application_load.py
import pytest
from PageObjects.MainPage import MainPage
from Configuration.Configuration import URL
from Utilities.Listeners import Listeners
from conftest import page, browser

listeners = None


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


class TestApplicationLoad:
    @pytest.mark.sanity
    @pytest.mark.parametrize("page_title", ["React App"])
    def test_application_loads_successfully(self, page_title, setup, page):
        main_page = setup
        assert main_page.get_page_title() == page_title, "Application failed to load"
