"""Пример определения доступных способов входа.

Функция get_login_methods() не требует авторизации —
можно узнать, как входить, до самого входа.
"""

import asyncio

from netschoolpy import get_login_methods, get_url, list_regions


async def main():
    # ── 1. Проверить конкретный сервер ─────────────────────
    print("=== Республика Мордовия ===")
    methods = await get_login_methods("https://sgo.e-mordovia.ru")
    print(f"  Версия:          {methods.version}")
    print(f"  Продукт:         {methods.product_name}")
    print(f"  Логин/пароль:    {methods.password}")
    print(f"  Госуслуги:       {methods.esia}")
    print(f"  Госуслуги осн.:  {methods.esia_main}")
    print(f"  Кнопка ЕСИА:     {methods.esia_button}")
    print(f"  → {methods.summary}")
    print()

    # ── 2. По имени региона ────────────────────────────────
    print("=== Челябинская область ===")
    methods = await get_login_methods("Челябинская область")
    print(f"  → {methods.summary}")
    print()

    # ── 3. Проверить все регионы ───────────────────────────
    print("=== Все регионы ===")
    for region in list_regions():
        url = get_url(region)
        if url is None:
            continue
        try:
            m = await get_login_methods(url, timeout=10)
        except Exception:
            print(f"  {region}: ❌ ошибка подключения")
            continue

        print(f"  {region}: {m.summary} (v{m.version})")


if __name__ == "__main__":
    asyncio.run(main())
