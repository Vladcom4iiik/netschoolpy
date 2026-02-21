# NetschoolPy

**NetschoolPy** – это асинхронная библиотека для работы с электронным дневником «Сетевой город. Образование» (NetSchool).

Библиотека полностью переписана и оптимизирована для удобного использования в современных Python проектах. Поддерживает вход как по логину/паролю от школы, так и через **Госуслуги (ESIA)**.

## Установка

```bash
pip install netschoolpy
```

## Быстрый старт

```python
import asyncio
from netschoolpy import NetSchoolAPI

async def main():
    ns = NetSchoolAPI('https://netschool.example.com')
    await ns.login('login', 'password', 'school_name')
    
    diary = await ns.diary()
    print(diary)
    
    await ns.logout()

if __name__ == '__main__':
    asyncio.run(main())
```
