# Продвинутое использование

## Работа с вложениями (Attachments)

NetSchool часто содержит файлы, прикреплённые к домашним заданиям. Вложения находятся внутри заданий (`Assignment`), а задания — внутри уроков (`Lesson`).

```python
diary = await ns.diary()
for day in diary.schedule:
    for lesson in day.lessons:
        for assignment in lesson.assignments:
            if assignment.attachments:
                for attachment in assignment.attachments:
                    print(f"Найдено вложение: {attachment.name} (ID: {attachment.id})")
                    # Скачивание файла:
                    # from io import BytesIO
                    # buf = BytesIO()
                    # await ns.download_attachment(attachment.id, buf)
```

## Кастомные периоды

Вы можете запрашивать дневник не только на текущую неделю, но и на любой произвольный промежуток времени.

```python
import datetime

# Получить дневник за сентябрь
start = datetime.date(2025, 9, 1)
end = datetime.date(2025, 9, 30)

month_diary = await ns.diary(start=start, end=end)
print(f"Всего уроков за месяц: {sum(len(d.lessons) for d in month_diary.schedule)}")
```

## Работа с несколькими учениками (Родительский аккаунт)

*Функционал в разработке.* Если аккаунт является родительским и привязано несколько детей, API позволяет переключаться между ними.
