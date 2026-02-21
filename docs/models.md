# Модели данных

Библиотека возвращает данные в виде объектов (dataclasses). Это позволяет удобно работать с полями через точку, а не через словари.

## Diary (Дневник)

Объект `Diary` содержит информацию о расписании и уроках на неделю или выбранный период.

- `start` (datetime.date): Дата начала периода.
- `end` (datetime.date): Дата конца периода.
- `schedule` (List[Day]): Список учебных дней.

## Day (Учебный день)

- `day` (datetime.date): Дата.
- `lessons` (List[Lesson]): Список уроков за этот день.

## Lesson (Урок)

Представляет собой один слот в расписании.

- `day` (datetime.date): Дата урока.
- `start` (datetime.time): Время начала.
- `end` (datetime.time): Время окончания.
- `number` (int): Порядковый номер урока (1, 2, 3...).
- `subject` (str): Название предмета (например, "Алгебра").
- `room` (str): Кабинет.
- `assignments` (List[Assignment]): Список заданий к уроку.

## Assignment (Задание)

Домашнее задание, контрольная работа и другие типы заданий.

- `id` (int): ID задания.
- `kind` (str): Тип задания (например, "Контрольная работа", "Домашнее задание").
- `kind_abbr` (str): Сокращение типа (например, "К", "ДЗ", "Т").
- `content` (str): Текст задания.
- `comment` (str): Комментарий к оценке.
- `mark` (int | None): Оценка за задание (если есть).
- `weight` (int): Коэффициент (вес) оценки для средневзвешенного балла (по умолчанию 1).
- `is_duty` (bool): Оценка по долгу.
- `deadline` (datetime.date): Дата сдачи.
- `attachments` (List[Attachment]): Прикреплённые файлы.

## Attachment (Вложение)

Если к заданию или объявлению прикреплены файлы.

- `id` (int): ID файла.
- `name` (str): Имя файла.
- `description` (str): Описание.

## Announcement (Объявление)

- `name` (str): Заголовок.
- `author` (Author): Автор.
- `content` (str): Текст.
- `post_date` (datetime.datetime): Дата публикации.
- `attachments` (List[Attachment]): Прикреплённые файлы.

## Author (Автор)

- `id` (int): ID пользователя.
- `full_name` (str): ФИО.
- `nickname` (str): Ник.

## Message (Письмо)

Письмо внутренней почты Сетевого Города.

- `id` (int): ID письма.
- `subject` (str): Тема.
- `text` (str): Текст письма.
- `sent` (datetime.datetime): Дата отправки.
- `author_id` (int): ID автора.
- `author_name` (str): Имя автора.
- `to_names` (str): Кому адресовано (текст).
- `is_read` (bool): Прочитано ли.
- `mailbox` (str): Папка («Inbox», «Sent», «Draft», «Deleted»).
- `can_reply` (bool): Можно ли ответить.
- `can_forward` (bool): Можно ли переслать.
- `file_attachments` (List[Attachment]): Прикреплённые файлы.

## MailRecipient (Получатель)

Контакт, которому можно отправить письмо.

- `id` (str): Идентификатор получателя.
- `name` (str): ФИО.
- `organization_name` (str): Название организации.

## ShortSchool / School (Школа)

`ShortSchool` — краткая информация (название, ID, адрес).
`School` — полная карточка школы (директор, email, сайт, телефон и т.д.).
