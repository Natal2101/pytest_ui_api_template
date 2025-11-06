from selenium.webdriver import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


@allure.epic("UI Тесты сервиса доставки")
class MainPage:
    """
            Класс для работы с главной страницей сайта доставки еды.
            Содержит основные методы для взаимодействия с элементами страницы,
            такие как:
                + установление адреса доставки,
                + установка куки,
                + поиск товара,
                + выбор первого результата поиска,
                + добавление товара в корзину,
                + изменение количества товара в корзине,
                + очистка корзины.
    """

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.__url = base_url
        self.__driver = driver
        self.wait = WebDriverWait(self.__driver, 20)

    @allure.step("UI. Переход на главную страницу по указанному url")
    def go(self, full_url: str) -> None:
        self.__driver.get(full_url)

    @allure.step("UI. Указание адреса доставки: {address}")
    def delivery_address_indication(self, address: str, text: str) -> str:
        self.__driver.implicitly_wait(4)

        with allure.step("Нажатие на кнопку адреса"):
            container = self.__driver.find_element(
                By.CSS_SELECTOR, "div.r1d1jd5y")
            button_address = container.find_element(
                By.CSS_SELECTOR, ".a1a8ol1h")
            button_address.click()

        with allure.step("Ввод адреса: {address}"):
            input_address = self.__driver.find_element(By.CSS_SELECTOR,
                                                       "input.afdxd29.mr7w3hr")
            input_address.send_keys(Keys.CONTROL + "a")
            input_address.send_keys(Keys.DELETE)

            input_address.send_keys(address)

        with allure.step("Выбор адреса из подсказок"):
            self.__driver.find_element(By.CSS_SELECTOR,
                                       "input.afdxd29.mr7w3hr").click()

            self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  ".react-autosuggest__suggestion."
                                                  "react-autosuggest__suggestion--first"))
            ).click()

        with allure.step("Подтверждение выбора адреса"):
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".r1jyb6b1.s1v4x2t8.v102ekr4."
                                      "syv67cr.o16sqpc5"))
            ).click()

        with allure.step("Ожидание обновления адреса на странице"):
            self.wait.until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, ".f18sb35s"),
                    text
                )
            )

        return (f"{self.__driver.find_element(
            By.CSS_SELECTOR, ".f18sb35s").text}"
                f"{self.__driver.find_element(
                    By.CSS_SELECTOR, ".skasrc6").text}")

    @allure.step("UI. Установка cookies")
    def set_cookies(self, cookies: list) -> None:
        for cookie in cookies:
            self.__driver.add_cookie(cookie)

    @allure.step("UI. Поиск товара: {product_for_search}")
    def search_product(self, product_for_search: str) -> str:
        with allure.step("Ввод текста в поисковую строку"):
            search_input = self.__driver.find_element(By.CSS_SELECTOR, "#id_1")
            search_input.clear()
            search_input.send_keys(product_for_search)

        with allure.step("Нажатие кнопки поиска"):
            self.__driver.find_element(By.CSS_SELECTOR,
                                       "button.r1jyb6b1.slw94yn."
                                       "v102ekr4.syv67cr.r1qlonej").click()

        with allure.step("Ожидание результатов поиска"):
            results_found = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".r1vfw7r0.p1dc8c6s.twh9z2q."
                                      "e19w8w8m.t1db1e91"))
            )

        return results_found.text

    @allure.step("UI. Выбор первого результата из списка")
    def select_result(self) -> str:

        list_results = self.__driver.find_elements(By.CSS_SELECTOR,
                                                   "button.f1d17p5r")
        first_result = list_results[0]
        aria_label = first_result.get_attribute("aria-label")
        with allure.step(f"Нажатие на товар: {aria_label}"):
            first_result.click()

        return aria_label

    @allure.step("UI. Добавление товара в корзину")
    def adding_item_to_cart(self) -> str:
        self.__driver.implicitly_wait(5)
        with allure.step("Нажатие кнопки добавления в корзину"):
            self.__driver.find_element(By.CSS_SELECTOR,
                                       "button.r1jyb6b1.slw94yn."
                                       "v102ekr4.syv67cr.cnts9l4").click()

        with allure.step("Нажатие кнопки оформления заказа"):
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "button.r1jyb6b1.slw94yn.v102ekr4."
                                      "syv67cr.cnts9l4.ftcyuun"))
            ).click()

        with allure.step("Получение названия товара в корзине"):
            product = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".ipy4n5l"))
            ).text

        return product

    @allure.step("UI. Очистка корзины")
    def clear_cart(self) -> None:
        with allure.step("Нажатие кнопки очищения корзины"):
            self.__driver.find_element(By.CSS_SELECTOR,
                                       ".mvl7tin.r1mbrood.t1i0hqyb").click()

        with allure.step("Нажатие кнопки подтверждения очищения корзины"):
            self.__driver.find_element(By.CSS_SELECTOR,
                                       ".r1orm7zp.st0n1t4.v102ekr4."
                                       "shkwuuz").click()

    @allure.step("UI. Увеличение количества товара до {number_for_increase}")
    def increase_number_by_digit(self, number_for_increase: str) -> str:
        with allure.step("Изменение количества товара"):
            quantity_goods = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".i16pn8aq.i1mttuda"))
            )
            quantity_goods.send_keys(Keys.CONTROL + "a")
            quantity_goods.send_keys(Keys.DELETE)
            quantity_goods.send_keys(number_for_increase)
            quantity_goods.click()

        with allure.step("Получение значения количества товара"):
            increased_quantity = quantity_goods.get_attribute("value")

        return increased_quantity

    @allure.step("UI. Уменьшение количества товара")
    def reduce_number_by_minus(self) -> str:
        with allure.step("Ожидание появления элемента"):
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".i16pn8aq.i1mttuda"))
            )
        with allure.step("Нажатие кнопки уменьшения"):
            self.__driver.find_element(By.CSS_SELECTOR,
                                       ".r1orm7zp.s1v4x2t8.vjiwpdh.shkwuuz."
                                       "izq4n4a.sbb4el8").click()

        self.__driver.implicitly_wait(2)

        with allure.step("Получение значения количества товара"):
            quantity_goods = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".i16pn8aq.i1mttuda"))
            )
            reduced_quantity = quantity_goods.get_attribute("value")

        return reduced_quantity
