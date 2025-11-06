import allure
from page.MainPage import MainPage
from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider

config = ConfigProvider("test_config.ini")
provider = DataProvider("test_data.json")


@allure.feature("Работа с адресом доставки")
@allure.story("Указание адреса доставки")
@allure.severity("BLOCKER")
@allure.title("Позитивный сценарий: указание адреса доставки")
@allure.description("""
Тест проверяет корректное указание адреса доставки через UI.
Ожидается:
    - Успешная установка адреса
    - Отображение правильного адреса на странице
""")
def test_delivery_address_indication(browser):
    try:
        main_page = MainPage(browser, config.get_ui_base_url())
        full_url = (f"{config.get_ui_base_url()}"
                    f"{provider.get_ui_url_krasnoyarsk()}")
        main_page.go(full_url)
        input_address = main_page.delivery_address_indication(
            provider.get_ui_address(), provider.get_ui_text())

        with allure.step("Проверка соответствия ожидаемого "
                         "результата фактическому"):
            assert input_address == provider.get_ui_address(), \
                "❌ Адрес доставки не установлен"

        print("✅✅✅✅✅✅Тест test_delivery_address_indication "
              "пройден успешно!✅✅✅✅✅✅")

    except Exception as e:
        print(f"❌❌❌❌❌❌Произошла ошибка "
              f"в test_delivery_address_indication: {str(e)}❌❌❌❌❌❌")
        raise


@allure.feature("Работа с корзиной")
@allure.story("Добавление товара в корзину")
@allure.severity("CRITICAL")
@allure.title("Позитивный сценарий: добавление товара в корзину")
@allure.description("""
Тест проверяет полный сценарий добавления товара в корзину:
    - Поиск товара
    - Выбор товара из результатов
    - Добавление в корзину
    - Проверка корректности добавленного товара
""")
def test_adding_item_to_cart(browser):
    try:
        main_page = MainPage(browser, config.get_ui_base_url())
        full_url = (f"{config.get_ui_base_url()}"
                    f"{provider.get_ui_url_krasnoyarsk()}")
        main_page.go(full_url)
        cookies = [
            {'name': config.get_name_token(),
             'value': config.get_value_token(),
             'domain': config.get_domain()},
            {'name': config.get_name_login(),
             'value': config.get_value_login(),
             'domain': config.get_domain()}
        ]
        main_page.set_cookies(cookies)
        browser.refresh()

        # получаем результат из строки поиска
        results_found = main_page.search_product(provider.get_ui_product_for_search())
        with allure.step("Проверка получения результатов поиска"):
            assert (str(results_found.split(',')[0].strip()) !=
                    "Ничего не нашли"), "❌ Результатов не найдено"
            assert int(results_found.split(' ')[1].strip()) > 0

        # выбираем товар, чтобы добавить его в корзину
        aria_label = main_page.select_result()
        with allure.step("Проверка совпадения поиска с результатом"):
            assert provider.get_ui_product_for_search().lower() in aria_label.lower(), \
                (f"❌ В названии выбранного варианта нет запрашиваемых "
                 f"слов *{provider.get_ui_product_for_search()}*")

        # добавляем товар в корзину
        product = main_page.adding_item_to_cart()
        with allure.step("Проверка совпадения поиска с товаром в корзине"):
            assert provider.get_ui_product_for_search().lower() in product.lower(), \
                (f"❌ В названии товара в корзине нет запрашиваемых "
                 f"слов *{provider.get_ui_product_for_search()}*")

            # expected_parts = aria_label.split(' ')
            # for part in expected_parts:
            #     assert part in product

            expected1 = str(aria_label.split(' ')[0].strip())
            expected2 = str(aria_label.split(' ')[1].strip())
            expected3 = str(aria_label.split(' ')[2].strip())
            assert expected1 in product and expected2 in product and expected3 in product

        print("✅✅✅✅✅✅Тест test_adding_item_to_cart "
              "пройден успешно!✅✅✅✅✅✅")

        # очищаем корзину
        main_page.clear_cart()

    except Exception as e:
        print(f"❌❌❌❌❌❌Произошла ошибка "
              f"в test_adding_item_to_cart: {str(e)}❌❌❌❌❌❌")
        raise


@allure.feature("Работа с корзиной")
@allure.story("Изменение количества товара")
@allure.severity("NORMAL")
@allure.title("Позитивный сценарий: увеличение количества товара "
              "путем изменения цифры")
@allure.description("""
Тест проверяет увеличение количества товара в корзине.
Ожидается:
    - Корректное изменение количества
    - Сохранение изменений
""")
def test_increase_quantity_goods(browser):
    try:
        main_page = MainPage(browser, config.get_ui_base_url())
        full_url = (f"{config.get_ui_base_url()}"
                    f"{provider.get_ui_url_krasnoyarsk()}")
        main_page.go(full_url)
        cookies = [
            {'name': config.get_name_token(),
             'value': config.get_value_token(),
             'domain': config.get_domain()},
            {'name': config.get_name_login(),
             'value': config.get_value_login(),
             'domain': config.get_domain()}
        ]
        main_page.set_cookies(cookies)
        browser.refresh()

        # получаем результат из строки поиска
        results_found = main_page.search_product(
            provider.get_ui_product_for_search())
        with allure.step("Проверка получения результатов поиска"):
            assert (str(results_found.split(',')[0].strip()) !=
                    "Ничего не нашли"), "❌ Результатов не найдено"
            assert int(results_found.split(' ')[1].strip()) > 0

        # выбираем товар, чтобы добавить его в корзину
        aria_label = main_page.select_result()
        with allure.step("Проверка совпадения поиска с результатом"):
            assert provider.get_ui_product_for_search().lower() in aria_label.lower(), \
                (f"❌ В названии выбранного варианта нет запрашиваемых "
                 f"слов *{provider.get_ui_product_for_search()}*")

        # добавляем товар в корзину
        product = main_page.adding_item_to_cart()
        with allure.step("Проверка совпадения поиска с товаром в корзине"):
            assert provider.get_ui_product_for_search().lower() in product.lower(), \
                (f"❌ В названии товара в корзине нет запрашиваемых "
                 f"слов *{provider.get_ui_product_for_search()}*")

        # увеличиваем количество товара в корзине
        increased_quantity = (main_page.increase_number_by_digit
                              (provider.get_ui_number_for_increase()))
        with allure.step("Проверка совпадения ожидаемого "
                         "результата с фактическим"):
            assert increased_quantity == provider.get_ui_number_for_increase(), \
                "❌ Количество товара не увеличено"

        print("✅✅✅✅✅✅Тест test_increase_quantity_goods "
              "пройден успешно!✅✅✅✅✅✅")

        # очищаем корзину
        main_page.clear_cart()

    except Exception as e:
        print(f"❌❌❌❌❌❌Произошла ошибка "
              f"в test_increase_quantity_goods: {str(e)}❌❌❌❌❌❌")
        raise


@allure.feature("Работа с корзиной")
@allure.story("Изменение количества товара")
@allure.severity("NORMAL")
@allure.title("Позитивный сценарий: уменьшение количества товара "
              "кнопкой минус")
@allure.description("""
Тест проверяет уменьшение количества товара в корзине.
Ожидается:
    - Корректное уменьшение количества
    - Сохранение изменений
""")
def test_reduce_quantity_goods(browser):
    try:
        main_page = MainPage(browser, config.get_ui_base_url())
        full_url = (f"{config.get_ui_base_url()}"
                    f"{provider.get_ui_url_krasnoyarsk()}")
        main_page.go(full_url)
        cookies = [
            {'name': config.get_name_token(),
             'value': config.get_value_token(),
             'domain': config.get_domain()},
            {'name': config.get_name_login(),
             'value': config.get_value_login(),
             'domain': config.get_domain()}
        ]
        main_page.set_cookies(cookies)
        browser.refresh()

        # получаем результат из строки поиска
        results_found = main_page.search_product(
            provider.get_ui_product_for_search())
        with allure.step("Проверка получения результатов поиска"):
            assert (str(results_found.split(',')[0].strip()) !=
                    "Ничего не нашли"), "❌ Результатов не найдено"
            assert int(results_found.split(' ')[1].strip()) > 0

        # выбираем товар, чтобы добавить его в корзину
        aria_label = main_page.select_result()
        with allure.step("Проверка совпадения поиска с результатом"):
            assert provider.get_ui_product_for_search().lower() in aria_label.lower(), \
                (f"❌ В названии выбранного варианта нет запрашиваемых "
                 f"слов *{provider.get_ui_product_for_search()}*")

        # добавляем товар в корзину
        product = main_page.adding_item_to_cart()
        with (allure.step("Проверка совпадения поиска с товаром в корзине")):
            assert provider.get_ui_product_for_search().lower() in product.lower(), \
                (f"❌ В названии товара в корзине нет запрашиваемых "
                 f"слов *{provider.get_ui_product_for_search()}*")

        # увеличиваем количество товара в корзине
        increased_quantity = (main_page.increase_number_by_digit
                              (provider.get_ui_number_for_increase()))
        with allure.step("Проверка увеличения количества товара"):
            assert increased_quantity == provider.get_ui_number_for_increase(), \
                "❌ Количество товара не увеличено"

        # Уменьшаем количество товара в корзине
        reduced_quantity = main_page.reduce_number_by_minus()
        with allure.step("Проверка совпадения ожидаемого "
                         "результата с фактическим"):
            assert int(reduced_quantity) < int(
                provider.get_ui_number_for_increase()), \
                "❌ Уменьшение количества не произошло"

            assert int(reduced_quantity) == int(
                provider.get_ui_number_for_increase()) - 1

        print("✅✅✅✅✅✅Тест test_reduce_quantity_goods пройден"
              " успешно!✅✅✅✅✅✅")

        # очищаем корзину
        main_page.clear_cart()

    except Exception as e:
        print(f"❌❌❌❌❌❌Произошла ошибка "
              f"в test_reduce_quantity_goods: {str(e)}❌❌❌❌❌❌")
        raise


@allure.feature("Поиск товаров")
@allure.story("Поиск несуществующего товара")
@allure.severity("MINOR")
@allure.title("Негативный сценарий: поиск несуществующего товара")
@allure.description("""
Тест проверяет обработку поиска несуществующего товара.
Ожидается:
   - Сообщение 'Ничего не нашли'
   - Отсутствие результатов поиска
""")
def test_non_existent_product(browser):
    try:
        main_page = MainPage(browser, config.get_ui_base_url())
        full_url = (f"{config.get_ui_base_url()}"
                    f"{provider.get_ui_url_krasnoyarsk()}")
        main_page.go(full_url)
        cookies = [
            {'name': config.get_name_token(),
             'value': config.get_value_token(),
             'domain': config.get_domain()},
            {'name': config.get_name_login(),
             'value': config.get_value_login(),
             'domain': config.get_domain()}
        ]
        main_page.set_cookies(cookies)
        browser.refresh()

        found_nothing = main_page.search_product(provider.get_ui_product_non())
        message = found_nothing.split(',')[0].strip()

        with allure.step("Проверка сообщения об отсутствии результатов"):
            assert message == "Ничего не нашли", \
                f"Ожидалось 'Ничего не нашли', но получено: {found_nothing}"

        print("✅✅✅✅✅✅Тест test_non_existent_product "
              "пройден успешно!✅✅✅✅✅✅")

    except Exception as e:
        print(f"❌❌❌❌❌❌Произошла ошибка "
              f"в test_non_existent_product: {str(e)}❌❌❌❌❌❌")
        raise
