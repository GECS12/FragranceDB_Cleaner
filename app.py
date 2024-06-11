from flask import Flask, request, render_template, jsonify
import sqlite3
import os
import db_utils

app = Flask(__name__)

DATABASE_NAME = 'PT_fragrances'
TABLES = ['PerfumesDigital', 'Perfumes24h', 'MassPerfumarias']

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
            cursor.execute(f'''
                SELECT "Brand", "Fragrance Name", "Quantity (ml)", "Price (€)", "Link", "Website"
                FROM {table}
                WHERE "Fragrance Name" LIKE ? OR "Website" LIKE ?
            ''', (query_str, query_str))
            results = cursor.fetchall()
            combined_results.extend(results)
        except sqlite3.OperationalError as e:
            print(f"Error querying table {table}: {e}")
    conn.close()
    return combined_results

def search_by_brand(brand):
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    brand_str = f'%{brand}%'
    combined_results = []
    for table in TABLES:
        try:
            cursor.execute(f'''
                SELECT "Brand", "Fragrance Name", "Quantity (ml)", "Price (€)", "Link", "Website"
                FROM {table}
                WHERE "Brand" LIKE ?
            ''', (brand_str,))
            results = cursor.fetchall()
            combined_results.extend(results)
        except sqlite3.OperationalError as e:
            print(f"Error querying table {table}: {e}")
    conn.close()
    return combined_results

def get_brand_suggestions(query):
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query_str = f'%{query}%'
    brands = set()
    for table in TABLES:
        try:
            cursor.execute(f'''
                SELECT DISTINCT "Brand"
                FROM {table}
                WHERE "Brand" LIKE ?
            ''', (query_str,))
            results = cursor.fetchall()
            for result in results:
                brands.add(result[0])
        except sqlite3.OperationalError as e:
            print(f"Error querying table {table}: {e}")
    conn.close()
    return sorted(list(brands))  # Sort the list of brands alphabetically

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '')
    suggestions = get_brand_suggestions(query)
    return jsonify(suggestions)

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ""
    results = []
    if request.method == 'POST':
        if 'brand' in request.form:
            query = request.form['brand']
            results = search_by_brand(query)
        else:
            query = request.form['query']
            results = search_fragrances(query)
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    db_path = get_database_path()
    for table in TABLES:
        db_utils.create_table(DATABASE_NAME, table)
    app.run(debug=True)
