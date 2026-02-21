import asyncio
import os
import sys
from netschoolpy import NetSchool

async def main():
    url = os.getenv("NS_URL", "https://sgo.your-region.ru")
    
    # SGO
    ns_login = os.getenv("NS_LOGIN")
    ns_password = os.getenv("NS_PASSWORD")
    ns_school = os.getenv("NS_SCHOOL")
    
    # ESIA
    esia_login = os.getenv("ESIA_LOGIN")
    esia_password = os.getenv("ESIA_PASSWORD")
    
    use_qr = "--qr" in sys.argv

    async with NetSchool(url) as ns:
        if use_qr:
            print("Вход через QR...")
            try:
                import qrcode
                async def qr_cb(data):
                    qr = qrcode.QRCode(); qr.add_data(data); qr.print_ascii()
                    print("Сканируйте QR!")
                await ns.login_via_gosuslugi_qr(qr_cb)
            except ImportError:
                print("pip install qrcode")
                return
        elif esia_login and esia_password:
            await ns.login_via_gosuslugi(esia_login, esia_password)
        elif ns_login and ns_password:
            await ns.login(ns_login, ns_password, ns_school)
        else:
            print("Нет данных (ENV NS_LOGIN/ESIA_LOGIN или --qr)")
            return

        diary = await ns.diary()
        print("Поиск вложений...")
        for day in diary.days:
            for user_lesson in day.lessons:
                 if user_lesson.attachments:
                     print(f"Предмет: {user_lesson.subject}")
                     for a in user_lesson.attachments:
                         print(f" - {a.name}")

if __name__ == "__main__":
    asyncio.run(main())
