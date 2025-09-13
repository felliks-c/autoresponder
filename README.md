API Документация
1. POST /auth/login – Логин пользователя

Описание:
Позволяет авторизовать пользователя. Если пользователя с указанным email нет — создаётся новый пользователь. Пароли хранятся в хэше. Возвращает access token (для быстрых запросов к сервису, хранится в Redis) и refresh token (для восстановления сессии, хранится в PostgreSQL).

URL: /auth/login
Метод: POST

Параметры запроса:

Параметр	Тип	Обязательный	Описание
email	string	да	Email пользователя
password	string	да	Пароль пользователя

Пример запроса:

POST /auth/login
{
  "email": "user@example.com",
  "password": "mypassword"
}


Пример ответа:

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
}


Ошибки:

401 Unauthorized — неправильные учётные данные.

500 Internal Server Error — не удалось создать пользователя.

2. POST /messages/send – Отправка сообщения

Описание:
Позволяет пользователю отправить текстовое сообщение.
Текст проходит через NLP-пайплайн, который возвращает ответ (response) и тип (type). В базе данных (MongoDB) сохраняется сообщение вместе с классификацией, а пользователю возвращается только response.

URL: /messages/send
Метод: POST

Заголовки:

Заголовок	Обязательный	Описание
Authorization	да	Bearer <access_token> или Bearer <refresh_token>

Параметры запроса:

Параметр	Тип	Обязательный	Описание
text	string	да	Текст сообщения

Пример запроса:

POST /messages/send
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
{
  "text": "Привет, как дела?"
}


Пример ответа:

{
  "response": "Здравствуйте! Чем могу помочь?"
}


Ошибки:

401 Unauthorized — токен не найден в Redis или PostgreSQL.

401 Unauthorized — некорректный формат заголовка Authorization.

3. GET /session/history – История сообщений пользователя

Описание:
Возвращает все сообщения пользователя, хранящиеся в базе MongoDB. Для каждого сообщения выводятся text и response.

URL: /session/history
Метод: GET

Заголовки:

Заголовок	Обязательный	Описание
Authorization	да	Bearer <access_token> или Bearer <refresh_token>

Пример запроса:

GET /session/history
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...


Пример ответа:

{
  "user_id": "1",
  "history": [
    {
      "id": "650c2f9d8c7a4f9b2f5e0f1a",
      "text": "Привет",
      "response": "Здравствуйте! Чем могу помочь?"
    },
    {
      "id": "650c2fa28c7a4f9b2f5e0f1b",
      "text": "Какая погода?",
      "response": "Сегодня солнечно"
    }
  ]
}


Ошибки:

401 Unauthorized — токен не найден или недействителен.



















Документация по проекту
Общая структура

Проект разделён на три основные части:

app – backend

frontend – frontend

other files – CI/CD и документация

Документация по app
Структура директорий и файлов:
1. api

Содержит маршруты и обработчики HTTP-запросов FastAPI.

Разделено по роутерам (auth.py, message.py, session.py) для логической группировки эндпоинтов.

Использует зависимости (Depends) для авторизации и получения текущего пользователя.

2. core

Содержит основные настройки и вспомогательные функции для работы приложения:

config.py – хранение конфигураций проекта, URL баз данных, секретных ключей, TTL для токенов.

security.py – функции хэширования пароля, проверки пароля, генерации access и refresh токенов.

logging.py – настройка логирования приложения.

3. crud

Функции создания, редактирования, поиска и удаления объектов всех баз данных (Postgres, MongoDB, Redis).

Взаимодействие с БД происходит через асинхронные функции.

Примеры:

sqlmodel.py – работа с Postgres через SQLModel. Функции: create_user, get_user_by_email, save_refresh_token.

motor.py – работа с MongoDB через Motor. Функции: create_message, get_message, get_user_messages.

redis.py – работа с Redis. Функции: save_access_token, get_user_by_token, create_session, delete_session.

4. db

Директория с логикой работы с базами данных и их моделями:

models.py – все модели БД представлены как Python-классы (SQLModel для Postgres, схемы для Mongo, структура для Redis).

postgres.py – инициализация и подключение к Postgres, настройка асинхронного engine и sessionmaker, создание таблиц при старте.

mongo.py – подключение к MongoDB через Motor, инициализация коллекций.

redis.py – подключение к Redis, настройка клиента с TTL для сессий.

5. nlp

Настройки NLP модели и функции её запуска. Остальной проект взаимодействует только через функцию nlp_pipeline.

embeddings.json – кеш интентов.

embeddings.py – работа с кешем интентов. Вызов из других частей проекта только через одну функцию.

intents.py – интенты представлены как Python-объекты.

pipeline.py – основной файл обработки запросов, асинхронная функция nlp_pipeline запускает обработку текста и возвращает ответ для пользователя.

6. Прочие файлы

.gitignore – игнорируемые файлы для Git.

Dockerfile – сборка и запуск контейнера приложения.

main.py – основной файл запуска FastAPI. Создаёт приложение, инициализирует все БД, подключает роутеры и задаёт lifespan.

requirements.txt – зависимости и библиотеки backend.