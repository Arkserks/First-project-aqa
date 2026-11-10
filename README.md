# First Project AQA

Фреймворк API-автотестов на стенд `bank_api` (Symfony + PostgreSQL, Docker).

Стек: **pytest** + **requests** + **Pydantic v2** + **SQLAlchemy 2** + **Allure** + **psycopg2**.

## Установка

Через **uv** (рекомендуется):

```bash
uv sync                      # поставит runtime + dev-зависимости из pyproject.toml
```

Через **pip**:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
pytest src/ -v                                   # весь набор
pytest src/main/api/create_user_test.py -v       # один файл
pytest src/ -m api                               # только API-тесты (маркер api)
```

Отчёт Allure:

```bash
pytest src/ --alluredir=src/allure-results
allure serve src/allure-results
```

> Каталог результатов Allure (`src/allure-results`) стоит чистить перед каждым прогоном:
> `rm -rf src/allure-results`. Иначе в отчёт попадают результаты прошлых прогонов, и Allure
> размножает тесты с рандомными параметрами (historyId считается от значений параметров).

## Конфигурация

`resources/urls.properties` — адреса и креды:

```properties
backendUrl=http://localhost:4111/api
dataBaseUrl=postgresql+psycopg2://symfony:password@localhost:5432/symfony_db
```

В рабочем проекте креды стоит вынести в переменные окружения — здесь они оставлены как есть,
чтобы стенд поднимался одной командой.

## Стенд

```bash
docker pull clausmerderet/bank_api:latest
docker run -d -p 4111:4111 -p 5432:5432 --name bank_api clausmerderet/bank_api:latest
```

Swagger UI: <http://localhost:4111/api/swagger> · спецификация: <http://localhost:4111/api/swagger.json>

## Структура

```
.
├── src/main/api/
│   ├── classes/api_manager.py       # точка входа: admin_steps + user_steps
│   ├── configs/config.py            # чтение resources/urls.properties
│   ├── db/                          # слой БД: engine, ORM-модели, crud
│   │   ├── engine.py
│   │   ├── base.py
│   │   ├── models/                  # user_table, account_table, credit_table, transaction_table
│   │   └── crud/                    # поиск записей БД по сценариям
│   ├── fixtures/                    # фикстуры pytest: предусловия и сборка запросов
│   ├── foundation/
│   │   ├── endpoint.py              # url + request_model + response_model для каждого эндпоинта
│   │   └── requesters/              # CrudRequester (транспорт) / ValidateCrudRequester (+ разбор ответа)
│   ├── geneartors/                  # генерация тестовых данных по CreationRule
│   ├── models/                      # Pydantic-модели запросов и ответов
│   ├── requests/                    # legacy-слой requester'ов
│   ├── specs/                       # request_specs (заголовки/логин), responce_specs (коды ответа)
│   ├── steps/                       # бизнес-шаги: create_user, create_account, create_deposit, ...
│   └── *_test.py                    # тесты
├── conftest.py                      # подключение фикстур к набору
├── pytest.ini
├── pyproject.toml                   # зависимости для uv
└── requirements.txt                 # зависимости для pip
```

## Как это устроено (коротко)

| Слой | Отвечает за |
|---|---|
| `models/` | контракт данных: поля запроса и ответа, alias'ы в camelCase |
| `geneartors/` | случайные **валидные** значения по правилу `CreationRule` |
| `specs/` | заголовки + авторизация (`request_specs`), ожидаемый код ответа (`responce_specs`) |
| `foundation/` | адрес эндпоинта + транспорт + разбор ответа в модель |
| `steps/` | бизнес-шаги: «создать юзера», «положить деньги», «перевести» |
| `fixtures/` | предусловия теста: создать юзера/счёт/кредит и собрать готовый запрос |
| `api_manager.py` | точка входа: `api_manager.admin_steps.*` / `api_manager.user_steps.*` |
| `db/` | доступ к БД стенда: ORM-модели и поиск записей по сценариям |

Тест — это **действие + проверки**; всё остальное живёт в слоях выше.
