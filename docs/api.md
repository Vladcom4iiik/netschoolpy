# API Reference

## NetSchoolAPI

Основной класс для взаимодействия с API.

### `__init__(url)`

Инициализирует клиент.

- `url` (str): URL вашего сервера NetSchool.

### `login(login, password, school, year=None)`

Авторизация пользователя.

- `login` (str): Логин пользователя.
- `password` (str): Пароль.
- `school` (str): Название школы (как в системе).
- `year` (str, optional): Учебный год.

### `diary(start=None, end=None)`

Получение дневника за указанный период.

- `start` (datetime.date, optional): Дата начала. По умолчанию – начало текущей недели.
- `end` (datetime.date, optional): Дата конца. По умолчанию – конец текущей недели.

### `logout()`

Завершение сессии.
