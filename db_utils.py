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
            "Quantity (ml)" INTEGER,  -- Ensure this is INTEGER
            "Price (€)" REAL,
            "Link" TEXT,
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


def insert_or_update_fragrance(db_name, table_name, brand, name, quantity, price, link, website):
    if fragrance_exists(db_name, table_name, name, quantity, price, link):
        print(
            f"Fragrance with name {name}, quantity {quantity}, price {price}, and link {link} already exists. Skipping insertion.")
    else:
        database_path = get_database_path(db_name)
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            INSERT INTO {table_name} ("Brand", "Fragrance Name", "Quantity (ml)", "Price (€)", "Link", "Website")
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (brand, name, quantity, price, link, website))
            conn.commit()
            print(
                f"Inserted fragrance: {brand}, name: {name}, quantity: {quantity}, price: {price}, link: {link}, website: {website}")


def insert_multiple_fragrances(db_name, table_name, fragrances):
    database_path = get_database_path(db_name)
    if table_exists(db_name, table_name):
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            # Explicitly cast Quantity (ml) to INTEGER
            for fragrance in fragrances:
                cursor.execute(f'''
                INSERT OR IGNORE INTO {table_name} ("Brand", "Fragrance Name", "Quantity (ml)", "Price (€)", "Link", "Website")
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (fragrance[0], fragrance[1], int(fragrance[2]), fragrance[3], fragrance[4], fragrance[5]))
                # Debugging: Print the exact SQL statement and data being executed
                #print(f'INSERT OR IGNORE INTO {table_name} ("Brand", "Fragrance Name", "Quantity (ml)", "Price (€)", "Link", "Website") VALUES ("{fragrance[0]}", "{fragrance[1]}", {int(fragrance[2])}, {fragrance[3]}, "{fragrance[4]}", "{fragrance[5]}")')
            conn.commit()
    else:
        print(f"Table {table_name} doesn't exist")


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


def verify_and_correct_schema(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Check the current schema
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    column_types = {column[1]: column[2] for column in columns}

    print(f"Current schema for {table_name}: {column_types}")

    # If the Quantity (ml) column is not INTEGER, alter the table
    if column_types.get('Quantity (ml)', '').upper() not in ('INTEGER', 'INT'):
        print(f"Altering {table_name} to change 'Quantity (ml)' to INTEGER")

        # Create a temporary table with the correct schema
        cursor.execute(f"""
            CREATE TABLE {table_name}_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Brand TEXT,
                Fragrance_Name TEXT,
                Quantity_ml INTEGER,
                Price_EURO REAL,
                Link TEXT,
                Website TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Copy data from the old table to the temporary table
        cursor.execute(f"""
            INSERT INTO {table_name}_temp (id, Brand, Fragrance_Name, Quantity_ml, Price_EURO, Link, Website, timestamp)
            SELECT id, Brand, Fragrance_Name, Quantity_ml, Price_EURO, Link, Website, timestamp
            FROM {table_name};
        """)

        # Drop the old table
        cursor.execute(f"DROP TABLE {table_name};")

        # Rename the temporary table to the original table name
        cursor.execute(f"ALTER TABLE {table_name}_temp RENAME TO {table_name};")

        print(f"Schema of {table_name} has been corrected.")

    conn.commit()
    conn.close()

