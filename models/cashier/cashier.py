from flask import Flask, current_app
from flask_mysqldb import MySQL

# Initialize Flask and MySQL
app = Flask(__name__)
app.config.from_object('config.Config')  # Load configuration
mysql = MySQL(app)

def get_cashier_invoices():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cashier_invoices")
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        current_app.logger.error(f"Error fetching invoices: {e}")
        return []
