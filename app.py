from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # User root
app.config['MYSQL_PASSWORD'] = ''  # No password
app.config['MYSQL_DB'] = 'hospital_management_system'
  # DB name for your POS system

mysql = MySQL(app)

# Set a secret key (replace with a long, random, unique string)
app.config['SECRET_KEY'] = 'Hiroshan1999'

@app.route('/', methods=['GET', 'POST'])
def dashbord():
   

    return render_template('base.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        try: #handle error
            password = request.form['password']
            email = request.form['email']
           

            cur = mysql.connection.cursor()
            # Fetch the admin user usingg email
            cur.execute("SELECT * FROM admin WHERE email = %s", (email,))
            admin_user = cur.fetchone()
            cur.close()

            print("check -->",admin_user)  

            # Check admin credi..
            if admin_user and admin_user[1] == password:
                return redirect(url_for('admin_dashbord'))  # Redirect to admin panel
            else:
                flash('Invalid email or password.')
                return redirect(url_for('dashbord'))  # Redirect to home if failed
        except Exception as e:
            flash('An error occurred: ' + str(e))
            return redirect(url_for('dashbord'))  # Redirect to home on error

    return render_template('admin.html')  

@app.route('/admin_dashbord')
def admin_dashbord():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM stock")
    stock=cur.fetchall()
    return render_template('admin_dashbord.html',stock=stock)


if __name__ == "__main__":
    app.run(debug=True)  


