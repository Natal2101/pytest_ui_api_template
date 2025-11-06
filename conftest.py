import pytest
from selenium import webdriver
import allure

from configuration.ConfigProvider import ConfigProvider
from api.DeliveryApi import DeliveryApi


@pytest.fixture(scope="session")
def browser():
    with allure.step("Открыть и настроить браузер"):
        config = ConfigProvider()
        timeout = config.get_ui_timeout()

        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.geolocation": 2}
        options.add_experimental_option("prefs", prefs)

        browser = webdriver.Chrome(options=options)
        browser.implicitly_wait(timeout)
        browser.maximize_window()
        yield browser

    with allure.step("Закрыть браузер"):
        browser.quit()


@pytest.fixture()
def delivery_api() -> DeliveryApi:
    config = ConfigProvider()
    url = config.get_api_base_url()
    return DeliveryApi(url)
