# Руководство пользователя

## Авторизация

Для работы с API необходимо авторизоваться. Поддерживается:
1.  Обычная авторизация (логин/пароль, выданные в школе).
2.  Авторизация через **Госуслуги (ESIA)** — логин/пароль или QR-код.

### Обычный вход

```python
from netschoolpy import NetSchool

async with NetSchool('https://your-netschool-url.ru') as ns:
    await ns.login('student_login', 'password', 'School Name')
```

### Вход через Госуслуги

Подробнее см. в разделе [Вход через Госуслуги](esia_login.md).

```python
await ns.login_via_gosuslugi('gosuslugi_login', 'gosuslugi_password')
```

## Получение дневника

Основная функция – получение дневника.

```python
diary = await ns.diary()  # Текущая неделя
```

Можно указать конкретные даты:

```python
import datetime
start = datetime.date(2025, 9, 1)
end = datetime.date(2025, 9, 7)
diary = await ns.diary(start, end)
```

Дневник содержит список дней в поле `schedule`:

```python
for day in diary.schedule:
    print(f"Дата: {day.day}")
    for lesson in day.lessons:
        print(f"  {lesson.number}. {lesson.subject}")
        for assignment in lesson.assignments:
            if assignment.mark:
                print(f"     Оценка: {assignment.mark}")
```

## Обработка ошибок

Библиотека выбрасывает исключения в случае ошибок авторизации или сети.

```python
from netschoolpy import NetSchool
from netschoolpy.exceptions import LoginError, SchoolNotFound

try:
    await ns.login(...)
except LoginError:
    print("Ошибка входа")
except SchoolNotFound:
    print("Школа не найдена")
```
