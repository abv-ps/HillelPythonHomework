import sqlite3

students = [
    ('Небийвлоб', 'Роман', '+38 063 456-4524', 'Бокс'),
    ('Питайло', 'Йосип', '+38 096 454-7591','Соціологія'),
    ('Чиставода', 'Надія','','Екологія'),
    ('Коливанов', 'Євген', '', 'Фізика'),
    ('Забийгвіздок', 'Микола', '', 'Праця')
]

conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    specialty TEXT)''')
conn.commit()
cursor.executemany('''INSERT INTO students (surname, name, phone, specialty) VALUES (?, ?, ?, ?)''', students)
conn.commit()
cursor.execute('''DELETE FROM students WHERE id > 5''')
conn.commit()
cursor.execute('SELECT * FROM students')
rows = cursor.fetchall()
for row in rows:
    print(row)
cursor.close()
conn.close()
