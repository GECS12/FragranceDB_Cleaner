import sqlite3
import pandas as pd
import os

def get_database_path(db_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', f'{db_name}.db')

def create_table(db_name, table_name):
    database_path = get_database_path(db_name)
    os.makedirs(os.path.dirname(database_path), exist_ok=True)  # Create directory if it doesn't exist
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            "Brand" TEXT,
            "Fragrance Name" TEXT,
            "Quantity (ml)" TEXT,
            "Price (€)" REAL,
            "Link" TEXT UNIQUE,
            "Website" TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()

def table_exists(db_name, table_name):
    database_path = get_database_path(db_name)
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
        ''', (table_name,))
        return cursor.fetchone() is not None

def fragrance_exists(db_name, table_name, name, price, link):
    database_path = get_database_path(db_name)
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        SELECT 1 FROM {table_name}
        WHERE "Fragrance Name" = ? AND "Price (€)" = ? AND "Link" = ?
        ''', (name, price, link))
        return cursor.fetchone() is not None

def insert_or_update_fragrance(db_name, table_name, name, price, quantity, link, website):
    if fragrance_exists(db_name, table_name, name, price, link):
        print(f"Fragrance with name {name}, price {price}, and link {link} already exists. Skipping insertion.")
    else:
        database_path = get_database_path(db_name)
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            INSERT INTO {table_name} ("Brand", "Fragrance Name", "Quantity (ml)", "Price (€)", "Link", "Website")
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, price, quantity, link, website))
            conn.commit()
            print(f"Inserted fragrance: {name}, price: {price}, quantity: {quantity}, link: {link}, website: {website}")

def insert_multiple_fragrances(db_name, table_name, fragrances):
    database_path = get_database_path(db_name)
    if table_exists(db_name, table_name):
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(f'''
            INSERT OR IGNORE INTO {table_name} ("Brand", "Fragrance Name", "Quantity (ml)", "Price (€)", "Link", "Website")
            VALUES (?, ?, ?, ?, ?, ?)
            ''', fragrances)
            conn.commit()
            print(f"Inserted {cursor.rowcount} fragrances into {table_name}")
    else:
        print("Table" + str(table_name) + "doesn't exist")

def print_database_contents(db_name, table_name):
    database_path = get_database_path(db_name)
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"Contents of {table_name}:")
        for row in rows:
            print(row)

def drop_table(db_name, table_name):
    database_path = get_database_path(db_name)
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        conn.commit()
        print(f"Table {table_name} has been dropped.")

def clean_quantity_column(db_name, table_name):
    database_path = get_database_path(db_name)
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        UPDATE {table_name}
        SET "Quantity (ml)" = CAST("Quantity (ml)" AS INTEGER)
        WHERE "Quantity (ml)" = CAST("Quantity (ml)" AS INTEGER)
        ''')
        conn.commit()
        print(f"Cleaned the Quantity (ml) column in table {table_name}")
