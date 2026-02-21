# Руководство пользователя

## Авторизация

Для работы с API необходимо авторизоваться. Поддерживается как обычная авторизация по логину/паролю, так и через ESIA (Госуслуги) в будущем (функционал в разработке).

```python
from netschoolpy import NetSchoolAPI

ns = NetSchoolAPI('https://your-netschool-url.ru')
await ns.login('student_login', 'password', 'School Name')
```

## Получение дневника

Основная функция – получение дневника.

```python
diary = await ns.diary() # Текущая неделя
```

Можно указать конкретные даты:

```python
import datetime
start = datetime.date(2023, 9, 1)
end = datetime.date(2023, 9, 7)
diary = await ns.diary(start, end)
```

## Обработка ошибок

Библиотека выбрасывает исключения в случае ошибок авторизации или сети.

```python
from netschoolpy import AnthError, NetSchoolAPI

try:
    await ns.login(...)
except AuthError:
    print("Ошибка входа")
```
