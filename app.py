import csv
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_file
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to import CSV data into the database
def import_csv_to_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Clear existing data (optional)
    c.execute('DELETE FROM inventory')

    # Read and import data from CSV
    with open('inventory.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            c.execute('''INSERT INTO inventory (product_name, quantity, price, product_type, sales) 
                         VALUES (?, ?, ?, ?, ?)''',
                      (row['product_name'], row['quantity'], row['price'], row['product_type'], row['sales']))

    conn.commit()
    conn.close()
    print("CSV data imported successfully!")

# Route to display the inventory and a search form
@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM inventory').fetchall()
    conn.close()
    return render_template('index.html', items=items)

# Route to add a new item
@app.route('/add', methods=('GET', 'POST'))
def add_item():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        price = request.form['price']
        product_type = request.form['product_type']
        sales = request.form['sales']

        conn = get_db_connection()
        conn.execute('INSERT INTO inventory (product_name, quantity, price, product_type, sales) VALUES (?, ?, ?, ?, ?)',
                     (product_name, quantity, price, product_type, sales))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_item.html')

# Route to search for items in the inventory
@app.route('/search', methods=('GET', 'POST'))
def search():
    query = request.form.get('query')

    conn = get_db_connection()
    items = conn.execute("SELECT * FROM inventory WHERE product_name LIKE ?", ('%' + query + '%',)).fetchall()
    conn.close()

    return render_template('index.html', items=items)

# Route to display the pie chart of sales by product type
@app.route('/sales_by_product_type')
def sales_by_product_type():
    conn = get_db_connection()
    data = conn.execute('SELECT product_type, SUM(sales) AS total_sales FROM inventory GROUP BY product_type').fetchall()
    conn.close()

    # Extract data for plotting
    product_types = [row['product_type'] for row in data]
    sales = [row['total_sales'] for row in data]

    # Create pie chart
    fig, ax = plt.subplots()
    ax.pie(sales, labels=product_types, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    # Save the plot to a BytesIO object and send it as a response
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    import_csv_to_db()  # Import CSV data when the app starts
    app.run(debug=True)
