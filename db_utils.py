import sqlite3
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
            "Fragrance Name" TEXT,
            "Quantity (ml)" INTEGER,
            "Price (€)" REAL,
            "Link" TEXT UNIQUE,
            "Website" TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()

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
            INSERT INTO {table_name} ("Fragrance Name", "Price (€)", "Quantity (ml)", "Link", "Website")
            VALUES (?, ?, ?, ?, ?)
            ''', (name, price, quantity, link, website))
            conn.commit()
            print(f"Inserted fragrance: {name}, price: {price}, quantity: {quantity}, link: {link}, website: {website}")

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



# Step 1: Read the Excel file
#excel_file_path = r'D:\Drive Folder\FragrancesV2\fragrancePT_Cleaner\fragranceDB\scrapers\fragrances.xlsx'  # Replace with your Excel file path
#df = pd.read_excel(excel_file_path)

# Step 2: Connect to the SQLite database (or create it)
#conn = sqlite3.connect('data/fragrance_database.db')  # Replace with your database file path

# Step 3: Insert data into the database
#table_name = 'PerfumesDigital'  # Replace with your desired table name
#df.to_sql(table_name, conn, if_exists='replace', index=False)

# Close the connection
#conn.close()

#print("Data has been successfully inserted into the database.")

