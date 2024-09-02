import sqlite3

# Create a SQLite database and connect
conn = sqlite3.connect('ignore/mission_data.db')
cursor = conn.cursor()

# Create the main table
cursor.execute('''
CREATE TABLE IF NOT EXISTS secret_info (
    id INTEGER PRIMARY KEY,
    description TEXT,
    data TEXT
)
''')

# Insert data into the secret_info table
cursor.execute("INSERT INTO secret_info (description, data) VALUES (?, ?)", ("Operation Details", "Top Secret: Infiltration Plan"))
cursor.execute("INSERT INTO secret_info (description, data) VALUES (?, ?)", ("Commander", "Ali Hassan"))
cursor.execute("INSERT INTO secret_info (description, data) VALUES (?, ?)", ("Server Info", "192.168.1.1"))
cursor.execute("INSERT INTO secret_info (description, data) VALUES (?, ?)", ("Location", "Ramallah"))
cursor.execute("INSERT INTO secret_info (description, data) VALUES (?, ?)", ("Note", "The email is hidden within this table, look carefully."))

# Hide the email in an unexpected field
cursor.execute("INSERT INTO secret_info (description, data) VALUES (?, ?)", ("Top Secret", "darwish@hamas.aza"))

# Create a table for agent details
cursor.execute('''
CREATE TABLE IF NOT EXISTS agents (
    agent_id INTEGER PRIMARY KEY,
    name TEXT,
    codename TEXT,
    assignment TEXT
)
''')

# Insert data into the agents table
cursor.execute("INSERT INTO agents (name, codename, assignment) VALUES (?, ?, ?)", ("John Doe", "Eagle", "Reconnaissance"))
cursor.execute("INSERT INTO agents (name, codename, assignment) VALUES (?, ?, ?)", ("Jane Smith", "Falcon", "Surveillance"))
cursor.execute("INSERT INTO agents (name, codename, assignment) VALUES (?, ?, ?)", ("Ali Hassan", "Wolf", "Operation Lead"))

# Create a table for communications
cursor.execute('''
CREATE TABLE IF NOT EXISTS communications (
    comm_id INTEGER PRIMARY KEY,
    comm_type TEXT,
    details TEXT
)
''')

# Insert data into the communications table
cursor.execute("INSERT INTO communications (comm_type, details) VALUES (?, ?)", ("Radio Frequency", "Encrypted channel 17.5 MHz"))
cursor.execute("INSERT INTO communications (comm_type, details) VALUES (?, ?)", ("Satellite", "Secure Sat-Comm"))
cursor.execute("INSERT INTO communications (comm_type, details) VALUES (?, ?)", ("Internal Memo", "Use 'Eagle' as the key in all transmissions"))

# Create a table for equipment
cursor.execute('''
CREATE TABLE IF NOT EXISTS equipment (
    equip_id INTEGER PRIMARY KEY,
    item TEXT,
    status TEXT
)
''')

# Insert data into the equipment table
cursor.execute("INSERT INTO equipment (item, status) VALUES (?, ?)", ("Drones", "Operational"))
cursor.execute("INSERT INTO equipment (item, status) VALUES (?, ?)", ("Night Vision Goggles", "Functional"))
cursor.execute("INSERT INTO equipment (item, status) VALUES (?, ?)", ("Encrypted Phones", "In Use"))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Enhanced Database created successfully!")
