import sqlite3

def run_query(database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    print("Connected to secure Hamas Communication Database.")
    try:
        while True:
            # Prompt the user for an SQL query
            query = input("Enter your SQL query (or type 'exit' to quit): ")

            if query.lower() == 'exit':
                break
            if query.lower().__contains__("delete") or query.lower().__contains__("update"):
                print("Can't delete from or update database!")
                continue
            try:
                # Execute the query
                cursor.execute(query)

                # If it's a SELECT query, fetch and print the results
                if query.strip().lower().startswith("select"):
                    results = cursor.fetchall()
                    if results:
                        for row in results:
                            print(row)
                    else:
                        print("No results found.")
                else:
                    # Commit the changes for INSERT, UPDATE, DELETE queries
                    conn.commit()
                    print("Query executed successfully.")

            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        # Close the connection
        conn.close()
        print("Connection closed.")


def connect_db():
    # Path to your SQLite database
    database_path = 'mission_data.db'  # Replace with your database file path
    run_query(database_path)

if __name__ == "__main__":
    connect_db()
