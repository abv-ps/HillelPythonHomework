import sqlite3
from typing import List, Tuple

Product = Tuple[str, str, float, int]
Order = Tuple[int, int, int, float]

products_list: List[Product] = [
    ("MLK001", "Молоко", 30.5, 100),
    ("BRD002", "Хліб", 25.0, 50),
    ("SOUR003", "Сметана", 50.0, 30),
    ("EGG004", "Яйця", 60.0, 200),
    ("KEF005", "Кефір", 35.0, 80)
]

orders_list: List[Order] = [
    (1, 2, 5, 125.0),
    (2, 1, 3, 91.5),
    (3, 4, 10, 600.0),
    (4, 5, 2, 70.0),
    (5, 3, 1, 50.0)
]

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.executescript(
    '''
    CREATE TABLE IF NOT EXISTS products (
        id_tovar INTEGER PRIMARY KEY AUTOINCREMENT,
        art_tovar TEXT UNIQUE NOT NULL,
        name_tovar TEXT NOT NULL,
        price REAL CHECK(price >= 0) NOT NULL,
        qty INTEGER CHECK(qty >= 0) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS orders (
        id_order INTEGER PRIMARY KEY AUTOINCREMENT,
        id_tovar INTEGER NOT NULL,
        qty INTEGER CHECK(qty > 0) NOT NULL,
        total_sum_order REAL CHECK(total_sum_order >= 0) NOT NULL,
        FOREIGN KEY (id_tovar) REFERENCES products(id_tovar) ON DELETE CASCADE
    );
    '''
)

conn.commit()
conn.close()
