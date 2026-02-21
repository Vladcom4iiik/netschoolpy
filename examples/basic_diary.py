import asyncio
import os
from netschoolpy import NetSchool


async def main():
    # Получаем данные для входа из переменных окружения или захардкодим
    url = os.getenv("NS_URL", "https://sgo.your-region.ru")
    login = os.getenv("NS_LOGIN", "login")
    password = os.getenv("NS_PASSWORD", "password")
    school = os.getenv("NS_SCHOOL", "My School")

    ns = NetSchool(url)
    
    try:
        # Авторизация
        await ns.login(login, password, school)
        print("Успешный вход!")

        # Получение дневника
        diary = await ns.diary()
        
        print("\nРасписание на неделю:")
        for day in diary.days:
            print(f"\nExample Day: {day.date}")
            for lesson in day.lessons:
                print(f"  {lesson.number}. {lesson.subject} - {lesson.room}")
                if lesson.mark:
                    print(f"     Оценка: {lesson.mark}")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await ns.logout()
        await ns.close()


if __name__ == "__main__":
    asyncio.run(main())
