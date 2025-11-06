# pytest_ui_api_template

## Шаблон для автоматизации тестирования на python

### Шаги
1. Склонировать проект, используя команду в терминале интегрированной среды разработки: 
   - 'git clone https://github.com/Natal2101/pytest_ui_api_template.git'
2. Установить все зависимости, используя команду в терминале интегрированной среды разработки:
   - 'pip3 install -r requirements.txt'
3. Указать данные cookie:
   - открыть в браузере страницу "Деливери" по адресу: 'https://market-delivery.yandex.ru', 
   - авторизироваться,
   - открыть DevTools, варианты открытия:
     - с помощью горячих клавиш:
       - нажать на клавиатуре клавишу F12;
       - нажать одновременно клавиши на клавиатуре для Windows и Linux - Ctrl + Shift + I, для macOS -  Cmd + Option + I;
     - через контекстное меню:
       - кликнуть правой кнопкой мыши в любом месте веб-страницы,
       - в открывшемся меню --> «Просмотреть код», «Исследовать элемент» или «Проверить объект» (название может отличаться в зависимости от браузера); 
     - через меню браузера:
       - нажать на значок с тремя точками или тремя полосками в правом верхнем углу браузера,
       - в выпадающем меню --> «Дополнительные инструменты» (или «Дополнительные настройки»), --> «Инструменты разработчика»;
   - в DevTools --> вкладка "Application" --> "Storage" --> "Cookies" --> "https://market-delivery.yandex.ru";
   - в открывшихся cookies:
     - найти "Eats-Session", скопировать значение и вставить его в значение переменной "cookie_eat_session", находящейся в файле test_config.ini,
     - найти "Session_id", скопировать значение и вставить его в значение переменной "value_token", находящейся в файле test_config.ini,
     - найти "yandex_login", скопировать значение и вставить его в значение переменной "value_login", находящейся в файле test_config.ini,
4. Запустить тесты, используя команду в терминале интегрированной среды разработки:
   - для запуска только UI-тестов: 'pytest test/test_ui.py'
   - для запуска только API-тестов: 'pytest test/test_api.py'
   - для запуска всех тестов: 'pytest'
5. Сгенерировать отчет, используя команду в терминале интегрированной среды разработки: 'allure generate allure-files -o allure-report'
6. Открыть отчет, используя команду в терминале интегрированной среды разработки: 'allure open allure-report'

### Стек:
- pytest
- selenium
- webdriver-manager
- requests
- allure
- configparser
- json

### Структура:
pytest_ui_api_template:
- api/ - хелпер для работы с API
    - DeliveryApi.py - основной класс для API
- configuration/ -  провайдер настроек
    - ConfigProvider.py - класс для управления конфигурациями
- page/ - описание страниц
    - MainPage.py - главная страница
- test/ - тесты
    - test_ui.py - UI-тесты
    - test_api.py - API-тесты
- testdata/ - провайдер тестовых данных
    - DataProvider.py - провайдер данных
- conftest.py - настройки окружения тестирования
- test_config.ini - настройки для тестов
- test_data.json - данные для тестов

### Полезные ссылки:
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
- [Про configparsers](https://docs.python.org/3/library/configparser.html)
- [Про pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/)

[Финальный проект по ручному тестированию](https://qa65-0.yonote.ru/share/7f1b2a21-44a4-4db9-badb-5a4af75be6a9)
