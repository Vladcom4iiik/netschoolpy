import asyncio
import datetime
import os
from netschoolpy import NetSchool


async def main():
    url = os.getenv("NS_URL", "https://sgo.your-region.ru")
    login = os.getenv("NS_LOGIN", "login")
    password = os.getenv("NS_PASSWORD", "password")
    school = os.getenv("NS_SCHOOL", "My School")

    async with NetSchool(url) as ns:
        await ns.login(login, password, school)

        # Выбираем период (например, прошлый месяц)
        today = datetime.date.today()
        start = today.replace(day=1)  # Первое число текущего месяца
        # Для примера возьмем последние 30 дней
        start = today - datetime.timedelta(days=30)
        end = today

        print(f"Анализ оценок с {start} по {end}...")

        diary = await ns.diary(start=start, end=end)

        marks = []
        subjects_marks = {}

        for day in diary.days:
            for lesson in day.lessons:
                if lesson.mark:
                    marks.append(lesson.mark)
                    
                    if lesson.subject not in subjects_marks:
                        subjects_marks[lesson.subject] = []
                    subjects_marks[lesson.subject].append(lesson.mark)

        if marks:
            avg_all = sum(marks) / len(marks)
            print(f"\nСредний балл по всем предметам: {avg_all:.2f}")
            print(f"Всего оценок: {len(marks)}")
        else:
            print("\nОценок за период не найдено.")

        print("\nПо предметам:")
        for subject, sub_marks in subjects_marks.items():
            avg = sum(sub_marks) / len(sub_marks)
            print(f"  {subject}: {avg:.2f} ({len(sub_marks)} оценок)")


if __name__ == "__main__":
    asyncio.run(main())
