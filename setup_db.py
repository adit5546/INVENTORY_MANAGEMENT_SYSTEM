import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create the inventory table
c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )''')

def alter_table():
    conn = get_db_connection()
    c = conn.cursor()

    # Add new columns to the inventory table
    c.execute('ALTER TABLE inventory ADD COLUMN product_type TEXT')
    c.execute('ALTER TABLE inventory ADD COLUMN sales INTEGER')

    conn.commit()
    conn.close()
    print("Table altered successfully!")

# Run this function once to alter the table
alter_table()



def show_table_structure():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Query to show the table structure
    c.execute('PRAGMA table_info(inventory)')
    
    # Fetch and print the results
    columns = c.fetchall()
    for column in columns:
        print(column)

show_table_structure()

# Commit and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")

