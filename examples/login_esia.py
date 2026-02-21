import asyncio
import os
from netschoolpy import NetSchool


async def main():
    # Настройки
    url = os.getenv("NS_URL", "https://sgo.your-region.ru")
    
    # Логин и пароль от Госуслуг
    esia_login = os.getenv("ESIA_LOGIN", "79000000000")
    esia_password = os.getenv("ESIA_PASSWORD", "gosuslugi_pass")

    ns = NetSchool(url)
    
    try:
        print("Вход через Госуслуги (ESIA)...")
        
        # Метод login_via_gosuslugi проходит полный цикл авторизации
        await ns.login_via_gosuslugi(esia_login, esia_password)
        
        print("Успешный вход через ESIA!")
        
        diary = await ns.diary()
        print(f"Дневник получен. Уроков на неделе: {sum(len(d.lessons) for d in diary.schedule)}")

    except Exception as e:
        print(f"Ошибка входа: {e}")
    finally:
        await ns.logout()
        await ns.close()


if __name__ == "__main__":
    asyncio.run(main())
