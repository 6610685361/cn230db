import sqlite3
import os

def create_connection(db_file):
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    return sqlite3.connect(db_file)

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            name TEXT,
            capital TEXT,
            region TEXT,
            population INTEGER,
            area REAL
        )
    """)
    conn.commit()

def insert_country(conn, country):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO countries (name, capital, region, population, area)
        VALUES (?, ?, ?, ?, ?)
    """, (
        country.get('name', {}).get('common'),
        country.get('capital', [None])[0],
        country.get('region'),
        country.get('population'),
        country.get('area')
    ))
    conn.commit()
