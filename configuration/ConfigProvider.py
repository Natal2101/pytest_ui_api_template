import configparser
import allure


class ConfigProvider:
    """
        Класс для работы с конфигурационными данными из INI-файла.
        Обеспечивает централизованное управление настройками тестов.
    """

    def __init__(self, filename: str = 'test_config.ini') -> None:
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    # UI Section Methods
    @allure.step("Получение URL интерфейса")
    def get_ui_base_url(self) -> str:
        return self.config['ui'].get('base_url')

    @allure.step("Получение таймаута ожидания элементов интерфейса")
    def get_ui_timeout(self) -> int:
        return int(self.config['ui'].get('timeout'))

    @allure.step("Получение названия поля токена")
    def get_name_token(self) -> str:
        return self.config['ui'].get('name_token')

    @allure.step("Получение значения токена")
    def get_value_token(self) -> str:
        return self.config['ui'].get('value_token')

    @allure.step("Получение доменного имени")
    def get_domain(self) -> str:
        return self.config['ui'].get('domain')

    @allure.step("Получение имени поля логина")
    def get_name_login(self) -> str:
        return self.config['ui'].get('name_login')

    @allure.step("Получение значения логина")
    def get_value_login(self) -> str:
        return self.config['ui'].get('value_login')

    # API Section Methods
    @allure.step("Получение базового URL API")
    def get_api_base_url(self) -> str:
        return self.config['api'].get('base_url')

    @allure.step("Получение таймаута ожиданий API")
    def get_api_timeout(self) -> int:
        return int(self.config['api'].get('timeout'))

    @allure.step("Получение куки eat session")
    def get_api_cookie_eat_session(self) -> str:
        return self.config['api'].get('cookie_eat_session')
