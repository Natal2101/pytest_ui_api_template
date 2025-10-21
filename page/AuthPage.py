from selenium.webdriver.remote.webdriver import WebDriver

class AuthPage:

    def __init__(self, driver: WebDriver) -> None:
        self.__url = "https://passport.yandex.ru/auth?backpath=https%3A%2F%2Fmarket-delivery.yandex.ru%2Fmoscow%3FshippingType%3Ddelivery&origin=market-delivery.yandex.ru&retpath=https%3A%2F%2Fmarket-delivery.yandex.ru%2Fmoscow%3Fauth_from%3Dside_menu%26shippingType%3Ddelivery&theme=light"
        self.__driver = driver

    def go(self):
        self.__driver.get(self.__url)
