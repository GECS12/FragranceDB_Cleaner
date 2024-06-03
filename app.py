from flask import Flask, request, render_template
import sqlite3
import os
import db_utils

app = Flask(__name__)

DATABASE_NAME = 'PT_fragrances'
TABLES = ['PerfumesDigital']


def get_database_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', f'{DATABASE_NAME}.db')


def search_fragrances(query):
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query_str = f'%{query}%'
    combined_results = []

    for table in TABLES:
        try:
            #print(f"Searching in table: {table} for query: {query_str}")
            cursor.execute(f'''
                SELECT "Brand", "Fragrance Name", "Quantity (ml)", "Price (€)", "Link", "Website"
                FROM {table}
                WHERE "Fragrance Name" LIKE ? OR "Website" LIKE ?
            ''', (query_str, query_str))
            results = cursor.fetchall()
            #print(f"Results from {table}: {results}")
            combined_results.extend(results)
        except sqlite3.OperationalError as e:
            print(f"Error querying table {table}: {e}")

    conn.close()
    return combined_results


@app.route('/', methods=['GET', 'POST'])
def index():
    query = ""
    results = []
    if request.method == 'POST':
        query = request.form['query']
        #print(f"Received search query: {query}")
        results = search_fragrances(query)
        #print(f"Search results: {results}")
    return render_template('index.html', query=query, results=results)


if __name__ == '__main__':
    # Ensure the database path is correct
    db_path = get_database_path()
    #print(f"Using database at: {db_path}")

    # Initialize the database and tables if they don't  exist
    for table in TABLES:
        db_utils.create_table(DATABASE_NAME, table)

    # Verify database contents
    #for table in TABLES:
        #db_utils.print_database_contents(DATABASE_NAME, table)

    app.run(debug=True)
