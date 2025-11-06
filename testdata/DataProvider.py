import json
import allure


class DataProvider:
    """
       Класс для работы с тестовыми данными из JSON-файла.
       Обеспечивает параметризацию тестов и управление тестовыми данными.
    """

    def __init__(self, filename: str = 'test_data.json') -> None:
        with open(filename, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    # Методы для UI-теста
    @allure.step("Получение данных для ввода в url страницы")
    def get_ui_url_krasnoyarsk(self) -> str:
        return self.data['UI']['url_krasnoyarsk']

    @allure.step("Получение данных для теста доставки адреса")
    def get_ui_address(self) -> str:
        return self.data['UI']['address']

    @allure.step("Получение текста для теста ввода адреса")
    def get_ui_text(self) -> str:
        return self.data['UI']['text']

    @allure.step("Получение продукта для поиска в UI")
    def get_ui_product_for_search(self) -> str:
        return self.data['UI']['product_for_search']

    @allure.step("Получение числа для увеличения количества товара")
    def get_ui_number_for_increase(self) -> str:
        return self.data['UI']['number_for_increase']

    @allure.step("Получение ненайденного продукта для UI")
    def get_ui_product_non(self) -> str:
        return self.data['UI']['product_non']

    # Методы для API-теста
    @allure.step("Получение адреса для API")
    def get_api_address(self) -> str:
        return self.data['API']['address']

    @allure.step("Получение координат для API")
    def get_api_coordinates(self) -> list:
        return self.data['API']['coordinates']

    @allure.step("Получение долготы для API")
    def get_api_longitude(self) -> float:
        return self.data['API']['longitude']

    @allure.step("Получение широты для API")
    def get_api_latitude(self) -> float:
        return self.data['API']['latitude']

    @allure.step("Получение продукта для поиска в API")
    def get_api_product_for_search(self) -> str:
        return self.data['API']['product_for_api_search']

    @allure.step("Получение ненайденного продукта для API")
    def get_api_product_non_existent(self) -> str:
        return self.data['API']['product_non_existent']

    @allure.step("Получение списка магазинов для API")
    def get_api_shops(self) -> list:
        return self.data['API']['shops']
