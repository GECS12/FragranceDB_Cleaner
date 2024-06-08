from datetime import datetime

def scrape_to_excel(fragrances):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'fragrances_PT_{timestamp}.xlsx'
    fragrances.to_excel(filename, index=False)
    path = r"D:\Drive Folder\FragrancesV2\fragrancePT_Cleaner\fragranceDB\scrapers\PerfumesDigital"
    print(filename + " has been saved in " + path)

def scraped_to_db(fragrances):
    db_name = 'PT_fragrances'
    table_name = 'PerfumesDigital'
    db_utils.create_table(db_name, table_name)
    fragrances_tuples = [tuple(row) for row in fragrances[['Brand', 'Fragrance Name', 'Quantity (ml)', 'Price (€)', 'Link', 'Website']].to_records(index=False)]
    db_utils.insert_multiple_fragrances(db_name, table_name, fragrances_tuples)
    print("Data has been inserted into the database")

def scraped_to_db(fragrances):
    db_name = 'PT_fragrances'
    table_name = 'PerfumesDigital'
    db_utils.create_table(db_name, table_name)
    fragrances_tuples = [tuple(row) for row in fragrances[
        ['Brand', 'Fragrance Name', 'Quantity (ml)', 'Price (€)', 'Link', 'Website']].to_records(index=False)]
    db_utils.insert_multiple_fragrances(db_name, table_name, fragrances_tuples)
    print("Data has been inserted into the database")