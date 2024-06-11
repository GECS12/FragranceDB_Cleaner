from db_utils import drop_table

if __name__ == "__main__":
    table_name = 'MassPerfumarias'
    db_name = 'PT_fragrances'

    drop_table(db_name,table_name)