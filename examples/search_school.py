"""Пример поиска школы по названию (без авторизации).

Автономная функция search_schools() не требует логина —
удобно для выбора школы перед входом.
"""

import asyncio

from netschoolpy import search_schools, get_url, list_regions


async def main():
    # ── 1. Поиск по прямому URL сервера ────────────────────
    print("=== Поиск по URL ===")
    schools = await search_schools(
        "https://sgo.e-mordovia.ru",
        "Лицей",
    )
    for s in schools:
        print(f"  [{s.id}] {s.short_name} — {s.name}")

    # ── 2. Поиск по имени региона ──────────────────────────
    print("\n=== Поиск по имени региона ===")
    schools = await search_schools("Республика Мордовия", "Лицей")
    for s in schools:
        print(f"  [{s.id}] {s.short_name} — {s.name}")

    # ── 3. Поиск по всем регионам ──────────────────────────
    print("\n=== Поиск «Лицей №1» по всем регионам ===")
    for region in list_regions():
        url = get_url(region)
        if url is None:
            continue
        try:
            results = await search_schools(url, "Лицей №1", timeout=10)
        except Exception:
            print(f"  {region}: ошибка подключения")
            continue

        if results:
            print(f"  {region} ({url}):")
            for s in results:
                print(f"    [{s.id}] {s.short_name}")


if __name__ == "__main__":
    asyncio.run(main())
