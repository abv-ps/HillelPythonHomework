import csv
import sqlite3

with open('movies.csv', 'r') as file:
    reader = csv.reader(file)
    movies_list = list(reader)
    movies_list.pop(0) #Remove headlines

with open('actors.csv', 'r') as file:
    reader = csv.reader(file)
    actors_list = [actor[1:] for actor in list(reader)]
    actors_list.pop(0) #Remove headlines



    with sqlite3.connect('kinodb.db') as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS kinodb (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            release_year INT NOT NULL,
            genre TEXT NOT NULL
        ''')
        conn.commit()

        try:
            cursor.executemany('''
                INSERT INTO students (title, release_year, genre) VALUES (?, ?, ?)
                ''', movies_list)
            conn.commit()

        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")