import asyncio
import os
import sys
from netschoolpy import NetSchool


async def main():
    # Настройки приоритетов входа:
    # 1. QR-код (если запущен с --qr)
    # 2. ESIA Login/Password (если заданы ENV)
    # 3. SGO Login/Password (если заданы ENV)

    url = os.getenv("NS_URL", "https://sgo.your-region.ru")
    
    # SGO
    ns_login = os.getenv("NS_LOGIN")
    ns_password = os.getenv("NS_PASSWORD")
    ns_school = os.getenv("NS_SCHOOL")
    
    # ESIA
    esia_login = os.getenv("ESIA_LOGIN")
    esia_password = os.getenv("ESIA_PASSWORD")
    
    # Флаг для QR
    use_qr = "--qr" in sys.argv

    ns = NetSchool(url)
    
    try:
        if use_qr:
            print("Вход через QR-код Госуслуг...")
            
            # Проверка наличия qrcode
            try:
                import qrcode
            except ImportError:
                print("Ошибка: Для QR-входа нужно установить qrcode: pip install qrcode")
                return

            async def qr_callback(qr_data):
                qr = qrcode.QRCode()
                qr.add_data(qr_data)
                qr.print_ascii()
                print("\nОтсканируйте QR-код в приложении Госуслуги!")

            await ns.login_via_gosuslugi_qr(qr_callback)
            
        elif esia_login and esia_password:
            print("Вход через Госуслуги (Log/Pass)...")
            await ns.login_via_gosuslugi(esia_login, esia_password)
            
        elif ns_login and ns_password:
            print("Вход через логин/пароль школы...")
            await ns.login(ns_login, ns_password, ns_school)
            
        else:
            print("Не найдены данные для входа!")
            print("Укажите NS_LOGIN/NS_PASSWORD или ESIA_LOGIN/ESIA_PASSWORD")
            print("Или запустите с флагом --qr")
            return

        print("Успешный вход!")
        diary = await ns.diary()
        
        print("\nРасписание на неделю:")
        for day in diary.days:
            print(f"\nExample Day: {day.date}")
            for lesson in day.lessons:
                print(f"  {lesson.number}. {lesson.subject}")
                if lesson.mark:
                    print(f"     Оценка: {lesson.mark}")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await ns.logout()
        await ns.close()


if __name__ == "__main__":
    asyncio.run(main())
