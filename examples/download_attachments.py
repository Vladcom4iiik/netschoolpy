import asyncio
import os
from netschoolpy import NetSchool


async def main():
    url = os.getenv("NS_URL", "https://sgo.your-region.ru")
    login = os.getenv("NS_LOGIN", "login")
    password = os.getenv("NS_PASSWORD", "password")
    school = os.getenv("NS_SCHOOL", "My School")

    async with NetSchool(url) as ns:
        await ns.login(login, password, school)

        diary = await ns.diary()
        
        print("Поиск вложений в домашнем задании...")
        
        found = False
        for day in diary.days:
            for lesson in day.lessons:
                if lesson.attachments:
                    found = True
                    print(f"\nНайдено вложение по предмету: {lesson.subject}")
                    for att in lesson.attachments:
                        print(f"  Файл: {att.name} (ID: {att.id})")
                        print(f"  Описание: {att.description}")
                        
                        # Здесь можно реализовать скачивание, если API предоставляет метод
                        # Например: link = await ns.get_attachment_link(att)
                        # print(f"  Ссылка: {link}")

        if not found:
            print("Вложений на этой неделе не найдено.")


if __name__ == "__main__":
    asyncio.run(main())
