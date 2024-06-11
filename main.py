import sqlite3
import pandas as pd
import os

DATABASE_NAME = 'PT_fragrances'
TABLES = ['PerfumesDigital', 'Perfumes24h', 'MassPerfumarias']

def get_database_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', f'{DATABASE_NAME}.db')

def extract_to_excel(database_name, tables, output_path):
    database_path = get_database_path()
    with sqlite3.connect(database_path) as conn:
        writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
        for table in tables:
            try:
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                df.to_excel(writer, sheet_name=table, index=False)
                print(f"Extracted {table} to {output_path}")
            except Exception as e:
                print(f"Error extracting table {table}: {e}")
        writer.close()

if __name__ == '__main__':
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'database_export.xlsx')
    extract_to_excel(DATABASE_NAME, TABLES, output_path)
    print(f"Data has been exported to {output_path}")
