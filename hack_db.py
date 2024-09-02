import sqlite3
import re

# Connect to the SQLite database
conn = sqlite3.connect('ignore/mission_data.db')
cursor = conn.cursor()

# Function to retrieve all table names in the database
def get_table_names():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table[0] for table in tables]

# Function to retrieve all columns from a specific table
def get_columns(table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    return [column[1] for column in columns]

# Function to query all data from a specific table
def get_all_data(table_name):
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    return rows

# Function to find potential sensitive information
def find_sensitive_data(data):
    sensitive_info = []
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    for entry in data:
        for item in entry:
            if isinstance(item, str):
                # Search for email-like patterns
                if email_pattern.search(item):
                    sensitive_info.append(item)

    return sensitive_info

# Main function to break into the database
def hack_database():
    tables = get_table_names()
    print("Tables found in the database:", tables)

    all_sensitive_data = []

    for table in tables:
        print(f"\nExploring table: {table}")
        columns = get_columns(table)
        print(f"Columns in {table}: {columns}")

        data = get_all_data(table)
        print(f"Data in {table}:", data)

        sensitive_data = find_sensitive_data(data)
        if sensitive_data:
            print(f"Sensitive information found in {table}: {sensitive_data}")
            all_sensitive_data.extend(sensitive_data)

    if all_sensitive_data:
        print("\nPotential sensitive information discovered:")
        for info in all_sensitive_data:
            print(info)
    else:
        print("\nNo sensitive information found.")

# Run the hack
hack_database()

# Close the connection
conn.close()
