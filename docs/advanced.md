# Продвинутое использование

## Работа с вложениями (Attachments)

NetSchool часто содержит файлы, прикрепленные к домашним заданиям. Библиотека позволяет получить ссылки на них.

```python
diary = await ns.diary()
for day in diary.days:
    for lesson in day.lessons:
        if lesson.attachments:
            for attachment in lesson.attachments:
                print(f"Найдено вложение: {attachment.name}")
                # Скачивание файла (примерный код, зависит от реализации http клиента)
                # content = await ns.download(attachment)
```

## Кастомные периоды

Вы можете запрашивать дневник не только на текущую неделю, но и на любой произвольный промежуток времени.

```python
import datetime

# Получить дневник за сентябрь
start = datetime.date(2023, 9, 1)
end = datetime.date(2023, 9, 30)

month_diary = await ns.diary(start=start, end=end)
print(f"Всего уроков за месяц: {sum(len(d.lessons) for d in month_diary.days)}")
```

## Работа с несколькими учениками (Родительский аккаунт)

*Функционал в разработке.* Если аккаунт является родительским и привязано несколько детей, API позволяет переключаться между ними.

```python
# Получить список детей (студентов)
students = await ns.get_students()

# Выбрать конкретного ребенка по ID
await ns.select_student(students[0].id)
```
