"""
Тест входа через QR-код Госуслуг.
Сгенерирует QR-код и будет ждать сканирования.
"""
import asyncio
from netschoolpy import NetSchool


async def show_qr(qr_data: str):
    """Показывает QR-код в терминале."""
    print(f"\n📱 QR-код сгенерирован!")
    print(f"   Содержимое: {qr_data[:80]}...")

    try:
        import qrcode
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
        print("\n👆 Отсканируйте этот QR-код в приложении «Госуслуги»")
    except ImportError:
        print(f"\n   Данные для QR: {qr_data}")
        print("   pip install qrcode для отображения QR")

    print("⏳ Ожидание сканирования (до 3 мин)...\n")


async def main():
    async with NetSchool("https://sgo.example.ru") as ns:
        try:
            await ns.login_via_gosuslugi_qr(
                qr_callback=show_qr,
                qr_timeout=180,
            )

            print("\n✅ Вход через QR выполнен успешно!")
            print(f"   Student ID  : {ns._student_id}")
            print(f"   Access Token: {ns._access_token[:40]}...")

            diary = await ns.diary()
            print(f"   Дней в дневнике: {len(diary.schedule)}")

        except KeyboardInterrupt:
            print("\n⛔ Прервано пользователем")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()


asyncio.run(main())
