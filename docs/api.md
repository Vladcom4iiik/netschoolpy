# API Reference

## NetSchool

Основной класс для взаимодействия с API.

### `__init__(url, *, timeout=None)`

Инициализирует клиент.

- `url` (str): URL вашего сервера NetSchool (например, `https://sgo.example.ru`).
- `timeout` (int, optional): Таймаут HTTP-запросов (по-умолчанию 5 сек).

Поддерживает `async with`:

```python
async with NetSchool("https://sgo.example.ru") as ns:
    await ns.login(...)
```

### `login(user_name, password, school, *, timeout=None)`

Авторизация по логину/паролю SGO.

- `user_name` (str): Логин пользователя.
- `password` (str): Пароль.
- `school` (str | int): Название школы (или её ID).

### `login_via_gosuslugi(esia_login, esia_password, *, timeout=None)`

Вход через Госуслуги (ЕСИА) — программно, без браузера.

- `esia_login` (str): Логин Госуслуг (телефон, email или СНИЛС).
- `esia_password` (str): Пароль Госуслуг.

### `login_via_gosuslugi_qr(qr_callback=None, qr_timeout=120, *, timeout=None)`

Вход через QR-код Госуслуг.

- `qr_callback` (callable, optional): Async/sync функция, получающая deep-link для QR.
- `qr_timeout` (int): Таймаут ожидания сканирования (по-умолчанию 120 сек).

### `diary(start=None, end=None, *, timeout=None)`

Получение дневника за указанный период.

- `start` (datetime.date, optional): Дата начала. По умолчанию – начало текущей недели.
- `end` (datetime.date, optional): Дата конца. По умолчанию – конец текущей рабочей недели.
- Возвращает: `Diary`.

### `overdue(start=None, end=None, *, timeout=None)`

Получить просроченные задания. Возвращает `List[Assignment]`.

### `announcements(take=-1, *, timeout=None)`

Получить объявления. Возвращает `List[Announcement]`.

### `attachments(assignment_id, *, timeout=None)`

Получить вложения к заданию. Возвращает `List[Attachment]`.

### `school_info(*, timeout=None)`

Информация о школе. Возвращает `School`.

### `download_attachment(attachment_id, buffer, *, timeout=None)`

Скачать вложение в `BytesIO`-буфер.

### `download_profile_picture(user_id, buffer, *, timeout=None)`

Скачать аватар пользователя в `BytesIO`-буфер.

### `logout(*, timeout=None)`

Завершение сессии.

### `close(*, timeout=None)`

Завершение сессии и закрытие HTTP-клиента.
