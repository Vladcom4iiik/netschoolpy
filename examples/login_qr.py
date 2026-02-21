import asyncio
import os
import sys

try:
    import qrcode
except ImportError:
    print("Для работы этого примера установите библиотеку qrcode:")
    print("pip install netschoolpy[qr]")
    print("или pip install qrcode")
    sys.exit(1)

from netschoolpy import NetSchool


async def main():
    url = os.getenv("NS_URL", "https://sgo.your-region.ru")
    
    ns = NetSchool(url)
    
    # Callback-функция, которая будет вызвана библиотекой
    # Она получает строку `qr_data`, которую нужно превратить в QR-код
    async def my_qr_callback(qr_data: str):
        print("\nГенерация QR-кода...")
        qr = qrcode.QRCode()
        qr.add_data(qr_data)
        qr.print_ascii()  # Вывод QR-кода прямо в терминал
        print("\nОтсканируйте этот код в мобильном приложении Госуслуги -> Сканер")
        print("(Ожидание сканирования...)\n")

    try:
        print("Запуск входа через QR-код Госуслуг...")
        
        # Запускаем вход. Библиотека сама будет ждать, пока вы отсканируете код.
        await ns.login_via_gosuslugi_qr(qr_callback=my_qr_callback)
        
        print("QR-код успешно отсканирован! Вход выполнен.")
        
        diary = await ns.diary()
        print(f"Дневник загружен: {len(diary.days)} дней.")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await ns.logout()
        await ns.close()


if __name__ == "__main__":
    asyncio.run(main())
