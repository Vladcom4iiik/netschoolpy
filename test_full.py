"""
Полный интеграционный тест netschoolpy.
Проверяет ВСЁ: авторизацию (QR/ESIA/пароль), дневник, модели,
объявления, просроченные задания, вложения, школу и т.д.

Запуск:
    python test_full.py              # вход по QR (по-умолчанию)
    python test_full.py --qr         # вход по QR
    python test_full.py --esia       # вход через логин/пароль Госуслуг
    python test_full.py --password   # вход по логину/паролю школы

Переменные окружения:
    NS_URL           — URL сервера (обязательно)
    ESIA_LOGIN       — логин Госуслуг (для --esia)
    ESIA_PASSWORD    — пароль Госуслуг (для --esia)
    NS_LOGIN         — логин школы (для --password)
    NS_PASSWORD      — пароль школы (для --password)
    NS_SCHOOL        — название школы (для --password)
"""

import asyncio
import datetime
import os
import sys
import traceback
from io import BytesIO

# ─── Цвета ───────────────────────────────────────────────────────
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def ok(msg: str):
    print(f"  {GREEN}✅ {msg}{RESET}")


def fail(msg: str):
    print(f"  {RED}❌ {msg}{RESET}")


def info(msg: str):
    print(f"  {CYAN}ℹ️  {msg}{RESET}")


def section(title: str):
    print(f"\n{BOLD}{YELLOW}{'═' * 50}")
    print(f"  {title}")
    print(f"{'═' * 50}{RESET}")


results: list[tuple[str, bool, str]] = []


def check(name: str, passed: bool, detail: str = ""):
    results.append((name, passed, detail))
    if passed:
        ok(f"{name}" + (f" — {detail}" if detail else ""))
    else:
        fail(f"{name}" + (f" — {detail}" if detail else ""))


async def main():
    url = os.getenv("NS_URL", "")
    if not url:
        print(f"{RED}❌ Переменная NS_URL не задана!{RESET}")
        print("Пример: export NS_URL=https://sgo.example.ru")
        sys.exit(1)

    # Определяем метод входа
    args = set(sys.argv[1:])
    if "--esia" in args:
        method = "esia"
    elif "--password" in args:
        method = "password"
    else:
        method = "qr"

    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════════════════════╗")
    print(f"║     ПОЛНЫЙ ТЕСТ netschoolpy                      ║")
    print(f"║     URL: {url:<39s} ║")
    print(f"║     Метод: {method:<37s} ║")
    print(f"╚══════════════════════════════════════════════════╝{RESET}")

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 1: Импорты
    # ═══════════════════════════════════════════════════════════
    section("1. ИМПОРТЫ")

    try:
        from netschoolpy import NetSchool
        check("import NetSchool", True)
    except Exception as e:
        check("import NetSchool", False, str(e))
        sys.exit(1)

    try:
        from netschoolpy.exceptions import LoginError, SchoolNotFound, ServerUnavailable
        check("import exceptions", True, "LoginError, SchoolNotFound, ServerUnavailable")
    except Exception as e:
        check("import exceptions", False, str(e))

    try:
        from netschoolpy.models import (
            Diary, Day, Lesson, Assignment, Attachment,
            Announcement, Author, School, ShortSchool,
        )
        check("import models", True, "Diary, Day, Lesson, Assignment, ...")
    except Exception as e:
        check("import models", False, str(e))

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 2: Создание клиента
    # ═══════════════════════════════════════════════════════════
    section("2. СОЗДАНИЕ КЛИЕНТА")

    ns = NetSchool(url)
    check("NetSchool(url)", True, f"объект создан: {type(ns).__name__}")

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 3: Авторизация
    # ═══════════════════════════════════════════════════════════
    section("3. АВТОРИЗАЦИЯ")

    try:
        if method == "qr":
            info("Метод: QR-код Госуслуг")
            try:
                import qrcode
                check("import qrcode", True)
            except ImportError:
                check("import qrcode", False, "pip install qrcode")
                sys.exit(1)

            async def qr_callback(qr_data: str):
                print()
                qr = qrcode.QRCode(
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                )
                qr.add_data(qr_data)
                qr.make(fit=True)
                qr.print_ascii(invert=True)
                print(f"\n  {YELLOW}⚠️  QR-код действителен ~1 минуту!{RESET}")
                print(f"  {CYAN}📱 Откройте Госуслуги → Сканер → отсканируйте{RESET}")
                print(f"  {CYAN}⏳ Ожидание сканирования...{RESET}\n")

            signed_token = await ns.login_via_gosuslugi_qr(
                qr_callback=qr_callback,
                qr_timeout=180,
            )
            check("login_via_gosuslugi_qr", True, f"signed_token={signed_token[:30]}...")

        elif method == "esia":
            esia_login = os.getenv("ESIA_LOGIN", "")
            esia_password = os.getenv("ESIA_PASSWORD", "")
            if not esia_login:
                esia_login = input(f"  {CYAN}Логин Госуслуг (телефон/email/СНИЛС): {RESET}").strip()
            if not esia_password:
                import getpass
                esia_password = getpass.getpass(f"  {CYAN}Пароль Госуслуг: {RESET}").strip()
            if not esia_login or not esia_password:
                fail("Логин и/или пароль не введены")
                sys.exit(1)
            info(f"Метод: ESIA логин/пароль ({esia_login[:3]}***)")
            await ns.login_via_gosuslugi(esia_login, esia_password)
            check("login_via_gosuslugi", True)

        elif method == "password":
            ns_login = os.getenv("NS_LOGIN", "")
            ns_password = os.getenv("NS_PASSWORD", "")
            ns_school = os.getenv("NS_SCHOOL", "")
            if not ns_login or not ns_password:
                fail("NS_LOGIN / NS_PASSWORD не заданы")
                sys.exit(1)
            if ns_school.isdigit():
                ns_school = int(ns_school)
            info(f"Метод: логин/пароль школы ({ns_login})")
            await ns.login(ns_login, ns_password, ns_school)
            check("login()", True)

    except Exception as e:
        check(f"Авторизация ({method})", False, str(e))
        traceback.print_exc()
        await ns.close()
        _print_summary()
        sys.exit(1)

    # Проверяем внутреннее состояние после логина
    check("student_id установлен", ns._student_id > 0, f"student_id={ns._student_id}")
    check("year_id установлен", ns._year_id > 0, f"year_id={ns._year_id}")
    check("access_token установлен", bool(ns._access_token), f"at={ns._access_token[:20]}...")
    check("assignment_types загружены", len(ns._assignment_types) > 0,
          f"{len(ns._assignment_types)} типов")

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 4: Дневник (текущая неделя)
    # ═══════════════════════════════════════════════════════════
    section("4. ДНЕВНИК (текущая неделя)")

    try:
        diary = await ns.diary()
        check("diary() — вызов", True)
        check("diary.start — тип date", isinstance(diary.start, datetime.date), str(diary.start))
        check("diary.end — тип date", isinstance(diary.end, datetime.date), str(diary.end))
        check("diary.schedule — список", isinstance(diary.schedule, list),
              f"{len(diary.schedule)} дней")

        total_lessons = 0
        total_assignments = 0
        total_marks = 0
        subjects = set()

        for day in diary.schedule:
            check_day = isinstance(day.day, datetime.date) and isinstance(day.lessons, list)
            for lesson in day.lessons:
                total_lessons += 1
                subjects.add(lesson.subject)
                assert isinstance(lesson.number, int)
                assert isinstance(lesson.subject, str)
                assert isinstance(lesson.room, str)
                assert isinstance(lesson.start, datetime.time)
                assert isinstance(lesson.end, datetime.time)
                assert isinstance(lesson.assignments, list)
                for a in lesson.assignments:
                    total_assignments += 1
                    assert isinstance(a.id, int)
                    assert isinstance(a.kind, str)
                    assert isinstance(a.content, str)
                    assert isinstance(a.deadline, datetime.date)
                    assert isinstance(a.attachments, list)
                    if a.mark is not None:
                        assert isinstance(a.mark, int)
                        total_marks += 1

        check("Day/Lesson/Assignment — типы OK", True)
        info(f"Уроков: {total_lessons}, предметов: {len(subjects)}, "
             f"заданий: {total_assignments}, оценок: {total_marks}")
        if subjects:
            info(f"Предметы: {', '.join(sorted(subjects)[:5])}{'...' if len(subjects) > 5 else ''}")

    except Exception as e:
        check("diary()", False, str(e))
        traceback.print_exc()

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 5: Дневник (произвольный период)
    # ═══════════════════════════════════════════════════════════
    section("5. ДНЕВНИК (прошлая неделя)")

    try:
        last_monday = datetime.date.today() - datetime.timedelta(
            days=datetime.date.today().weekday() + 7
        )
        last_friday = last_monday + datetime.timedelta(days=4)
        diary2 = await ns.diary(start=last_monday, end=last_friday)
        check("diary(start, end)", True,
              f"{last_monday} — {last_friday}, {len(diary2.schedule)} дней")
    except Exception as e:
        check("diary(start, end)", False, str(e))

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 6: Просроченные задания
    # ═══════════════════════════════════════════════════════════
    section("6. ПРОСРОЧЕННЫЕ ЗАДАНИЯ")

    try:
        overdue = await ns.overdue()
        check("overdue()", True, f"{len(overdue)} заданий")
        if overdue:
            a = overdue[0]
            check("Assignment.id", isinstance(a.id, int), str(a.id))
            check("Assignment.kind", isinstance(a.kind, str), a.kind)
            check("Assignment.content", isinstance(a.content, str), a.content[:50] if a.content else "(пусто)")
    except Exception as e:
        check("overdue()", False, str(e))

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 7: Объявления
    # ═══════════════════════════════════════════════════════════
    section("7. ОБЪЯВЛЕНИЯ")

    try:
        announcements = await ns.announcements()
        check("announcements()", True, f"{len(announcements)} объявлений")
        if announcements:
            ann = announcements[0]
            check("Announcement.name", isinstance(ann.name, str), ann.name[:50])
            check("Announcement.author", isinstance(ann.author.full_name, str), ann.author.full_name)
            check("Announcement.post_date", isinstance(ann.post_date, datetime.datetime),
                  str(ann.post_date))
            check("Announcement.attachments", isinstance(ann.attachments, list),
                  f"{len(ann.attachments)} вложений")
    except Exception as e:
        check("announcements()", False, str(e))

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 8: Вложения к заданию
    # ═══════════════════════════════════════════════════════════
    section("8. ВЛОЖЕНИЯ К ЗАДАНИЮ")

    # Ищем первое задание с ID для теста
    test_assignment_id = None
    try:
        diary_for_attach = await ns.diary()
        for day in diary_for_attach.schedule:
            for lesson in day.lessons:
                for a in lesson.assignments:
                    if a.id and test_assignment_id is None:
                        test_assignment_id = a.id
    except Exception:
        pass

    if test_assignment_id:
        try:
            att_list = await ns.attachments(test_assignment_id)
            check("attachments(id)", True,
                  f"assignment_id={test_assignment_id}, вложений: {len(att_list)}")
            for att in att_list:
                check(f"Attachment #{att.id}", isinstance(att.name, str), att.name)
        except Exception as e:
            check("attachments(id)", False, str(e))
    else:
        info("Нет заданий для проверки вложений — пропускаем")

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 9: Информация о школе
    # ═══════════════════════════════════════════════════════════
    section("9. ИНФОРМАЦИЯ О ШКОЛЕ")

    try:
        school = await ns.school_info()
        check("school_info()", True, f"{school.name}")
        check("School.name — str", isinstance(school.name, str), school.name[:60])
        check("School.address — str", isinstance(school.address, str), school.address[:60])
    except Exception as e:
        check("school_info()", False, str(e))

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 10: Почта (mail)
    # ═══════════════════════════════════════════════════════════
    section("10. ПОЧТА")

    try:
        from netschoolpy.models import MailEntry, MailPage, Message
        check("import MailEntry, MailPage, Message", True)
    except Exception as e:
        check("import mail models", False, str(e))

    try:
        mail_page = await ns.mail_list(page_size=5)
        check("mail_list()", True, f"total={mail_page.total_items}, entries={len(mail_page.entries)}")
        check("MailPage.page", isinstance(mail_page.page, int), str(mail_page.page))
        check("MailPage.total_items", isinstance(mail_page.total_items, int), str(mail_page.total_items))

        if mail_page.entries:
            e0 = mail_page.entries[0]
            check("MailEntry.id — int", isinstance(e0.id, int), str(e0.id))
            check("MailEntry.subject — str", isinstance(e0.subject, str), e0.subject[:50])
            check("MailEntry.author — str", isinstance(e0.author, str), e0.author[:50])
    except Exception as e:
        check("mail_list()", False, str(e))
        traceback.print_exc()

    # mail_unread
    try:
        unread_ids = await ns.mail_unread()
        check("mail_unread()", True, f"{len(unread_ids)} непрочитанных")
    except Exception as e:
        check("mail_unread()", False, str(e))

    # mail_read — читаем первое письмо
    test_msg_id = None
    if mail_page.entries:
        test_msg_id = mail_page.entries[0].id
    if test_msg_id:
        try:
            msg = await ns.mail_read(test_msg_id)
            check("mail_read(id)", True, f"id={msg.id}, тема='{msg.subject[:40]}'")
            check("Message.text — str", isinstance(msg.text, str), f"{len(msg.text)} символов")
            check("Message.file_attachments — list", isinstance(msg.file_attachments, list),
                  f"{len(msg.file_attachments)} вложений")

            # Скачиваем первое вложение, если есть
            if msg.file_attachments:
                att = msg.attachments[0]
                buf = BytesIO()
                await ns.download_attachment(att.id, buf)
                check("download_attachment(mail)", buf.tell() > 0,
                      f"{att.name}, {buf.tell()} байт")
        except Exception as e:
            check("mail_read(id)", False, str(e))
            traceback.print_exc()
    else:
        info("Нет писем для чтения — пропускаем mail_read")

    # mail_recipients
    try:
        recipients = await ns.mail_recipients()
        check("mail_recipients()", True, f"{len(recipients)} получателей")
    except Exception as e:
        check("mail_recipients()", False, str(e))

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 11: Keep-alive
    # ═══════════════════════════════════════════════════════════
    section("11. KEEP-ALIVE")

    try:
        check("keepalive_task активен", ns._keepalive_task is not None and not ns._keepalive_task.done())
        ns.set_keepalive_interval(60)
        check("set_keepalive_interval(60)", ns._keepalive_interval == 60)
        ns.set_keepalive_interval(300)
        check("set_keepalive_interval(300) — сброс", ns._keepalive_interval == 300)
    except Exception as e:
        check("keep-alive", False, str(e))

    # ═══════════════════════════════════════════════════════════
    #  ТЕСТ 12: Выход
    # ═══════════════════════════════════════════════════════════
    section("12. ВЫХОД")

    try:
        await ns.logout()
        check("logout()", True)
    except Exception as e:
        check("logout()", False, str(e))

    try:
        await ns.close()
        check("close()", True)
    except Exception as e:
        check("close()", False, str(e))

    # ═══════════════════════════════════════════════════════════
    #  ИТОГИ
    # ═══════════════════════════════════════════════════════════
    _print_summary()


def _print_summary():
    passed = sum(1 for _, p, _ in results if p)
    failed = sum(1 for _, p, _ in results if not p)
    total = len(results)

    print(f"\n{BOLD}{'═' * 50}")
    print(f"  ИТОГО: {total} тестов")
    print(f"  {GREEN}✅ Пройдено: {passed}{RESET}")
    if failed:
        print(f"  {RED}❌ Провалено: {failed}{RESET}")
        print(f"\n  {RED}Провалившиеся:{RESET}")
        for name, p, detail in results:
            if not p:
                print(f"    {RED}• {name}: {detail}{RESET}")
    else:
        print(f"\n  {GREEN}{BOLD}🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!{RESET}")
    print(f"{BOLD}{'═' * 50}{RESET}\n")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    asyncio.run(main())
