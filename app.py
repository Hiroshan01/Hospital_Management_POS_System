from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hospital_management_system'

mysql = MySQL(app)

# Set a secret key (replace with a long, random, unique string)
app.config['SECRET_KEY'] = 'Hiroshan1999'

# Main Page Route
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Create a cursor and execute the query
    cursor = mysql.connection.cursor()
    query = "SELECT role FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()  # Fetch the first matching record
    
    if user:
        role = user[0]  # Access the role from the returned tuple
        session['username'] = username
        session['role'] = role

        # Role-based redirection
        if role == 'SuperAdmin':
            return redirect(url_for('superadmin_dashboard1'))
        elif role == 'Admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'User':
            return redirect(url_for('user_dashboard'))
        elif role == 'Cashier':
            return redirect(url_for('cashier_dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('home'))

# SuperAdmin Dashboard Route
@app.route('/superadmin_db_details')
def superadmin_dashboard1():
    # Fetch stock data
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM stock")  
    stock = cursor.fetchall()
    print(stock)  # Debugging output

    return render_template('superadmin_dashboard.html', stock=stock)

# Stock Update Route
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_stock(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        item_name = request.form['item-name']
        quantity = request.form['quantity']
        price = request.form['price']
        reorder_level = request.form['reorder-level']
        
        # Update stock in the database
        cur.execute("""
            UPDATE stock 
            SET item_name = %s, quantity = %s, price = %s, reorder_level = %s 
            WHERE id = %s""", (item_name, quantity, price, reorder_level, id))
        
        mysql.connection.commit()  # Save changes
        cur.close()  # Close the cursor
        return redirect(url_for('superadmin_dashboard1'))
    
    # If GET request, fetch the current stock data
    cur.execute("SELECT * FROM stock WHERE id = %s", (id,))
    stock = cur.fetchone()
    cur.close()
    return render_template('update_stock.html', stock=stock)

# Add Stock Route
@app.route('/add', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        item_name = request.form['item-name']
        quantity = request.form['quantity']
        price = request.form['price']
        reorder_level = request.form['reorder-level']
        
        cur = mysql.connection.cursor()  # Interact with DB
        cur.execute("INSERT INTO stock (item_name, quantity, price, reorder_level) VALUES (%s, %s, %s, %s)", 
                   (item_name, quantity, price, reorder_level))
        mysql.connection.commit()  # Save
        cur.close()  # Close the cursor
        return redirect(url_for('superadmin_dashboard1'))
    
    return redirect(url_for('superadmin_dashboard1'))

# Delete Stock Route
@app.route('/delete/<int:id>', methods=['GET'])
def delete_stock(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM stock WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()  # Close the cursor
    return redirect(url_for('superadmin_dashboard1'))

# Role-specific Dashboard Routes
@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard1.html')

@app.route('/user')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/cashier')
def cashier_dashboard():
    return render_template('user_dashboard.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out.')  # Optional: Add a flash message
    return redirect(url_for('home'))  # Redirect to the homepage or login

# Admin Dashboard Route
@app.route('/admin_dashboard_superadmin')
def super_admin_dashboard():
    return render_template('admin_dashboard.html')

#----------------User operation------------------#


if __name__ == '__main__':
    app.run(debug=True)
