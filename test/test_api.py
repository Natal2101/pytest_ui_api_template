import allure
from api.DeliveryApi import DeliveryApi
from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider

config = ConfigProvider("test_config.ini")
provider = DataProvider("test_data.json")


@allure.feature("Управление адресом доставки")
@allure.story("Изменение адреса доставки")
@allure.severity("CRITICAL")
@allure.title("Позитивный сценарий: проверка успешного "
              "изменения адреса доставки")
@allure.description("""
Тест проверяет успешное изменение адреса доставки через API.
Ожидается:
    - Статус код 200
    - Наличие ключа 'results' в ответе
    - Соответствие введенного адреса возвращенному
""")
def test_positive_change_delivery_address(delivery_api: DeliveryApi):
    try:
        data = {
            "action": "user_input",
            "type": "a",
            "part": provider.get_api_address(),
            "state": {
                "current_mode": "eats",
                "bbox": provider.get_api_coordinates()
            }
        }
        headers = {
            'cookie': config.get_api_cookie_eat_session(),
            'accept-language': 'ru'
        }
        changed_address = delivery_api.change_delivery_address(headers, data)

        with allure.step("Проверка статус кода"):
            assert changed_address.status_code == 200, \
                "❌ Адрес доставки не изменился"

        with allure.step("Проверка структуры ответа"):
            assert "results" in changed_address.json(), \
                "❌ Ответ не содержит ключ 'results'"

            results = changed_address.json()["results"]
            assert len(results) > 0, "❌ Результаты пусты"

        with allure.step("Проверка соответствия ожидаемого "
                         "результата фактическому"):
            assert changed_address.json()["results"][0]['title']['text'] == provider.get_api_address()

        print("✅✅✅✅✅✅Тест test_positive_change_delivery_address "
              "пройден успешно!✅✅✅✅✅✅")

    except Exception as e:
        print(f"❌❌❌❌❌❌Произошла ошибка "
              f"в test_positive_change_delivery_address: "
              f"{str(e)}❌❌❌❌❌❌")
        raise


@allure.feature("Поиск продуктов")
@allure.story("Поиск существующих товаров")
@allure.severity("CRITICAL")
@allure.title("Позитивный сценарий: поиск существующего продукта")
@allure.description("""
Тест проверяет успешный поиск товара через API.
Сценарий:
1. Установка адреса доставки
2. Поиск товара по названию
Ожидается:
    - Статус код 200
    - Наличие результатов поиска
    - Корректное отображение количества найденных товаров
""")
def test_positive_search_product(delivery_api: DeliveryApi):
    try:
        # указываем адрес доставки
        data = {
            "action": "user_input",
            "type": "a",
            "part": provider.get_api_address(),
            "state": {
                "current_mode": "eats",
                "bbox": provider.get_api_coordinates()
            }
        }
        headers = {
            'cookie': config.get_api_cookie_eat_session(),
            'accept-language': 'ru'
        }
        changed_address = delivery_api.change_delivery_address(headers, data)

        with allure.step("Проверка статус кода изменения адреса"):
            assert changed_address.status_code == 200, \
                "❌ Адрес доставки не изменился"

        # поиск через строку поиска
        token = f"{config.get_name_token()}={config.get_value_token()}"
        login = f"{config.get_name_login()}={config.get_value_login()}"
        cookie = f"{token}; {login}"

        headers = {
            'cookie': cookie,
            'accept-language': 'ru',
            'Authorization': f'Bearer {token}'
        }
        data = {
            "text": provider.get_api_product_for_search(),
            "filters": [],
            "location": {
                "longitude": provider.get_api_longitude(),
                "latitude": provider.get_api_latitude()
            }
        }
        found_product = delivery_api.search_product(headers, data)

        with allure.step("Проверка статус кода поиска товара"):
            assert found_product.status_code == 200, \
                "❌ Запрашиваемый товар не найден"

        with allure.step("Проверка результатов поиска"):
            founded_result = found_product.json()["header"]["text"]
            results = founded_result.split(' ')
            expected1, expected2, expected3 = results[0].lower(), results[1], results[2].lower()

            assert expected1.lower() == 'найдено'
            assert int(expected2) > 0
            assert expected3 in ['результатов',
                                 'результат', 'результата']

        print("✅✅✅✅✅✅Тест test_positive_search_product "
              "пройден успешно!✅✅✅✅✅✅")

    except Exception as e:
        print(f"❌❌❌❌❌❌Произошла ошибка "
              f"в test_positive_search_product:"
              f" {str(e)}❌❌❌❌❌❌")
        raise


@allure.feature("Поиск продуктов")
@allure.story("Поиск несуществующих товаров")
@allure.severity("MINOR")
@allure.title("Негативный сценарий: поиск несуществующего продукта")
@allure.description("""
Тест проверяет обработку поиска несуществующего товара.
Ожидается:
    - Статус код 200
    - Сообщение 'ничего не нашли' в ответе
    - Отсутствие результатов поиска
""")
def test_negative_search_non_existent_product(delivery_api: DeliveryApi):
    try:
        # указываем адрес доставки
        data = {
            "action": "user_input",
            "type": "a",
            "part": provider.get_api_address(),
            "state": {
                "current_mode": "eats",
                "bbox": provider.get_api_coordinates()
            }
        }
        headers = {
            'cookie': config.get_api_cookie_eat_session(),
            'accept-language': 'ru'
        }
        changed_address = delivery_api.change_delivery_address(headers, data)

        with allure.step("Проверка статус кода изменения адреса"):
            assert changed_address.status_code == 200, \
                "❌ Адрес доставки не изменился"

        # поиск через строку поиска
        token = f"{config.get_name_token()}={config.get_value_token()}"
        login = f"{config.get_name_login()}={config.get_value_login()}"
        cookie = f"{token}; {login}"
        headers = {
            'cookie': cookie,
            'accept-language': 'ru',
            'Authorization': f'Bearer {token}'
        }
        data = {
            "text": provider.get_api_product_non_existent(),
            "filters": [],
            "location": {
                "longitude": provider.get_api_longitude(),
                "latitude": provider.get_api_latitude()
            }
        }
        found_product = delivery_api.search_product(headers, data)

        with allure.step("Проверка статус кода поиска товара"):
            assert found_product.status_code == 200, \
                "❌ Запрашиваемый товар не найден"

        with allure.step("Проверка результатов поиска"):
            founded_product_text = found_product.json()["header"]["text"]
            if 'найдено' in founded_product_text.lower():
                assert False, f"❌ Ошибка: {founded_product_text}"

            expected = str(founded_product_text.split(',')[0].strip())

            assert expected.lower() == 'ничего не нашли'

        print("✅✅✅✅✅✅Тест "
              "test_negative_search_non_existent_product "
              "пройден успешно!✅✅✅✅✅✅")

    except Exception as e:
        print(f"❌❌❌❌❌❌Произошла ошибка "
              f"в test_negative_search_non_existent_product: "
              f"{str(e)}❌❌❌❌❌❌")
        raise


@allure.feature("Магазины")
@allure.story("Получение списка магазинов")
@allure.severity("CRITICAL")
@allure.title("Позитивный сценарий: получение списка магазинов")
@allure.description("""
Тест проверяет получение списка магазинов через API.
Сценарий:
    1. Установка адреса доставки
    2. Получение списка магазинов
Ожидается:
    - Статус код 200
    - Наличие магазинов в ответе
    - Присутствие ожидаемых магазинов в списке
""")
def test_positive_get_list_shops(delivery_api: DeliveryApi):
    try:
        # указываем адрес доставки
        data = {
            "action": "user_input",
            "type": "a",
            "part": provider.get_api_address(),
            "state": {
                "current_mode": "eats",
                "bbox": provider.get_api_coordinates()
            }
        }
        headers = {
            'cookie': config.get_api_cookie_eat_session(),
            'accept-language': 'ru'
        }
        changed_address = delivery_api.change_delivery_address(headers, data)

        with allure.step("Проверка статус кода изменения адреса"):
            assert changed_address.status_code == 200, \
                "❌ Адрес доставки не изменился"

        # получение списка магазинов
        token = f"{config.get_name_token()}={config.get_value_token()}"
        login = f"{config.get_name_login()}={config.get_value_login()}"
        cookie = f"{token}; {login}"
        headers = {
            'cookie': cookie,
            'x-device-id': 'mbf0psvl-9qggld7b7v-ochuyru1isk-kc50vstxhp',
            'accept-language': 'ru',
            'content-type': 'application/json;charset=UTF-8',
            'Authorization': f'Bearer {token}'
        }
        data = {
            "view": {
                "type": "collection",
                "slug": "shops"
            },
            "location": {
                "latitude": provider.get_api_latitude(),
                "longitude": provider.get_api_longitude()
            }
        }
        getting_list_shops = delivery_api.get_list_shops(headers, data)

        with allure.step("Проверка статус кода получения "
                         "списка магазинов"):
            assert getting_list_shops.status_code == 200, \
                "❌ Список магазинов не получен"

        with allure.step("Проверка списка магазинов"):
            all_shops = getting_list_shops.json()
            list_shops = all_shops["data"]["places_v2_lists"][0]["payload"]["places"]
            total_shops = len(list_shops)

            shop_names = [shop["name"]["value"] for shop in list_shops]

            assert total_shops > 0
            assert provider.get_api_shops()[0] in shop_names
            assert provider.get_api_shops()[1] in shop_names
            assert provider.get_api_shops()[2] in shop_names

        print("✅✅✅✅✅✅Тест test_positive_get_list_shops "
              "пройден успешно!✅✅✅✅✅✅")

    except Exception as e:
        print(f"❌❌❌❌❌❌Произошла ошибка "
              f"в test_positive_get_list_shops: "
              f"{str(e)}❌❌❌❌❌❌")
        raise


@allure.feature("Управление адресом доставки")
@allure.story("Изменение адреса доставки")
@allure.severity("MINOR")
@allure.title("Негативный сценарий: попытка удаления"
              " адреса доставки")
@allure.description("""
Тест проверяет обработку ошибки при попытке удалить адрес доставки
с пустыми координатами и адресом.
Ожидается:
   - Статус код 400
   - Соответствующее сообщение об ошибке
""")
def test_negative_removing_delivery_address(delivery_api: DeliveryApi):
    try:
        data = {
            "action": "user_input",
            "type": "a",
            "part": "",
            "state": {
                "current_mode": "eats",
                "bbox": []
            }
        }
        headers = {
            'cookie': config.get_api_cookie_eat_session(),
            'accept-language': 'ru'
        }
        removing_address = delivery_api.change_delivery_address(headers, data)

        with allure.step("Проверка статус кода удаления адреса доставки"):
            assert removing_address.status_code == 400, \
                (f"❌ Удаление адреса доставки прошло успешно, "
                 f"статус {removing_address.status_code}")

        with allure.step("Проверка содержимого сообщения об ошибке"):
            response_json = removing_address.json()
            expected_message_fragment = ("path 'state.bbox': "
                                         "incorrect size, must be 4 "
                                         "(limit) <= 0 (value)")

            assert expected_message_fragment in response_json.get("message", "")

        print("✅✅✅✅✅✅Тест test_negative_removing_delivery_address "
              "пройден успешно!✅✅✅✅✅✅")

    except Exception:
        print("❌❌❌❌❌❌ Произошла ошибка в "
              "test_negative_removing_delivery_address ❌❌❌❌❌❌")
        raise
