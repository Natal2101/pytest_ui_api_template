import requests
import allure
from requests import Response


@allure.epic("API Тесты сервиса доставки")
class DeliveryApi:
    """
            Класс для работы с веб-страницей сервиса доставки еды.
            Этот класс предоставляет методы для взаимодействия с сервисом.
            Включает в себя:
            + позитивные проверки:
                + изменение адреса доставки,
                + поиск существующего товара,
                + получение списка магазинов
            — негативные проверки:
                — поиск несуществующего товара,
                — удаление адреса доставки.
    """
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    @allure.step("API. Изменение адреса доставки")
    def change_delivery_address(self, headers: dict, data: dict) -> Response:
        path = '/eats/v1/persuggest/v1/suggest'
        resp = requests.post(f"{self.base_url}{path}",
                             headers=headers, json=data)
        return resp

    @allure.step("API. Поиск товара")
    def search_product(self, headers: dict, data: dict) -> Response:
        path = '/eats/v1/full-text-search/v1/search'
        resp = requests.post(f"{self.base_url}{path}",
                             headers=headers, json=data)
        return resp

    @allure.step("API. Получение списка магазинов")
    def get_list_shops(self, headers: dict, data: dict) -> Response:
        path = '/eats/v1/layout-constructor/v1/layout'
        resp = requests.post(
            f"{self.base_url}{path}", headers=headers, json=data)
        return resp
