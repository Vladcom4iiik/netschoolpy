# Руководство пользователя

## Авторизация

Для работы с API необходимо авторизоваться. Поддерживается:
1.  Обычная авторизация (логин/пароль, выданные в школе).
2.  Авторизация через **Госуслуги (ESIA)**.

### Обычный вход

```python
from netschoolpy import NetSchool

ns = NetSchool('https://your-netschool-url.ru')
await ns.login('student_login', 'password', 'School Name')
```

### Вход через Госуслуги

Подробнее см. в разделе [Вход через Госуслуги](esia_login.md).

```python
await ns.login_esia('gosuslugi_login', 'gosuslugi_password')
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
