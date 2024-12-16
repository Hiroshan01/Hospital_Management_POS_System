from flask import request, render_template, redirect, url_for, flash, current_app
from flask import Flask, current_app
from flask_mysqldb import MySQL
from flask import request

# Initialize Flask and MySQL
app = Flask(__name__)
app.config.from_object('config.Config')  # Load configuration
mysql = MySQL(app)

def search_user_route():
    users = []  # To hold search results
    if request.method == 'POST':
        phone_no = request.form['phone_no_search']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users_data WHERE phone_no = %s", (phone_no,))
        users = cur.fetchall()  # Get all matching users
        cur.close()
    
    return render_template('user/search_user.html', users=users)
