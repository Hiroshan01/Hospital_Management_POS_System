from flask import request, render_template, redirect, url_for, flash, current_app
from flask import Flask, current_app
from flask_mysqldb import MySQL
from flask import request

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
    
# Function to add a new invoice
def add_invoice(mysql):
    if request.method == 'POST':
        amount=request.form['amount']
        time=request.form['time']
        date=request.form['date']
        payment_method=request.form['payment_method']
        status=request.form['status']
        user_id=request.form['user_id']

        try:
            # Insert into the database
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO cashier_invoices (amount, time, date, payment_method, status, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (amount, time, date, payment_method, status, user_id))
            mysql.connection.commit()
            cursor.close()
            flash('Invoice added successfully!', 'success')
            return redirect(url_for('add_invoice_form'))
        except Exception as e:
            current_app.logger.error(f"Error adding invoice: {e}")
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('add_invoice_form'))

