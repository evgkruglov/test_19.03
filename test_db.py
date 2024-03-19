import random
import sqlite3
from datetime import datetime, timedelta

CREATE_TABLES = """
DROP TABLE if EXISTS 'SOTR';
CREATE TABLE 'SOTR' (
    sotr_id INTEGER PRIMARY KEY autoincrement,
    name VARCHAR(50) NOT NULL,
    mesto VARCHAR(50) NOT NULL,
    address VARCHAR(50) NOT NULL,
    sex CHAR(1) NOT NULL,
    birth_date DATE NOT NULL
);

DROP TABLE if EXISTS 'ZARP';
CREATE TABLE 'ZARP' (
    zarp_id INTEGER PRIMARY KEY autoincrement,
    name VARCHAR(50) NOT NULL,
    zarp INTEGER DEFAULT NULL
);

DROP TABLE if EXISTS 'PAYMENTS';
CREATE TABLE 'PAYMENTS' (
    pay_id INTEGER PRIMARY KEY autoincrement,
    name VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    amount REAL DEFAULT NULL
);
"""


def _get_random_birth_date() -> datetime:
    start_date = datetime(1975, 1, 1)
    end_date = datetime(1985, 12, 31)
    delta = end_date - start_date
    random_days_count = random.randint(0, delta.days)
    birth_date = start_date + timedelta(days=random_days_count)
    return birth_date


def _get_amount_date(month: int) -> datetime:
    day = 20
    month = month
    return datetime(2007, month, day)


families = """
Иванов
Васильев
Петров
Смирнов
Михайлов
Фёдоров
Соколов
Яковлев
Попов
Андреев
Алексеев
Александров
Лебедев
Григорьев
Степанов
Семёнов
Павлов
Богданов
Николаев
Дмитриев
Егоров
Волков
Кузнецов
Никитин
Соловьёв
""".split()

name_letters = "абвгдежзиклмнопрстуфхцчшщэюя".upper()


def _get_random_full_name() -> tuple:
    sex = random.choice(("M", "W"))

    family_name = random.choice(families)
    if sex == "W":
        family_name += "а"

    first_letter, last_letter = random.choice(name_letters), random.choice(name_letters)

    return f"{family_name} {first_letter}.{last_letter}.", sex


cities = """
Москва
Омск
Барнаул
Ярославль
Краснодар
Севастополь
Ялта
Сочи
Ижевск
Иркутск
Мурманск
Санкт-Петербург
Архангельск
""".split()


def prepare_tables():
    with sqlite3.connect("test.db") as conn:

        cursor = conn.cursor()
        cursor.executescript(CREATE_TABLES)
        conn.commit()

        employees = []
        for _ in range(30):
            name, sex = _get_random_full_name()
            address = random.choice(cities)
            mesto = random.choice(cities)
            birth_date = _get_random_birth_date()
            employees.append((name, address, mesto, sex, birth_date))

        conn.executemany(
            """
                INSERT INTO 'SOTR'(name, address, mesto, sex, birth_date)
                VALUES (?, ?, ?, ?, ?)
                """,
            employees,
        )

        salaries = []
        for employee in employees:
            name = employee[0]
            salary = random.randint(100, 900)
            salaries.append((name, salary))

        conn.executemany(
            """
                INSERT INTO 'ZARP'(name, zarp)
                VALUES (?, ?)
                """,
            salaries,
        )

        payments = []
        for month in range(1, 13):
            for employee, salary in zip(employees, salaries):
                name = employee[0]
                date = _get_amount_date(month)
                amount = salary[1]
                payments.append((name, date, amount))

        conn.executemany(
            """
                insert into 'PAYMENTS'(name, date, amount)
                values(?, ?, ?)
            """,
            payments,
        )
