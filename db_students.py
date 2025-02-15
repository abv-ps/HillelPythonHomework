"""
This module provides a function to create an SQLite database, populate it with student records,
and perform basic database operations like deleting certain records.

The student records include details such as surname, name, phone number, and specialty.
The function creates a database, sets up a table for storing student records, inserts the records,
deletes some based on a condition, and prints the remaining records.

Functions:
    create_and_populate_db(db_name: str, students: List[StudentRecord]) -> None:
        Creates a database, sets up a table, inserts student records, and deletes some records.
"""

import sqlite3
from typing import List, Tuple

StudentRecord = Tuple[str, str, str, str]

students_list: List[StudentRecord] = [
    ('Небийвлоб', 'Роман', '+38 063 456-4524', 'Бокс'),
    ('Питайло', 'Йосип', '+38 096 454-7591', 'Соціологія'),
    ('Чиставода', 'Надія', '', 'Екологія'),
    ('Коливанов', 'Євген', '', 'Фізика'),
    ('Забийгвіздок', 'Микола', '', 'Праця')
]


def create_and_populate_db(db_name: str, students: List[StudentRecord]) -> None:
    """
    Creates a database, sets up a table, inserts student records, and deletes some records.

    Args:
        db_name (str): The name of the SQLite database file.
        students (List[StudentRecord]): A list of tuples containing student records.

    Returns:
        None
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surname TEXT NOT NULL,
        name TEXT NOT NULL,
        phone TEXT,
        specialty TEXT
    )''')
    conn.commit()

    cursor.executemany('''
    INSERT INTO students (surname, name, phone, specialty) VALUES (?, ?, ?, ?)
    ''', students_list)
    conn.commit()

    cursor.execute('DELETE FROM students WHERE id > 5')
    conn.commit()

    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    conn.close()
