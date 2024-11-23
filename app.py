from flask import Flask, render_template, request, redirect, url_for, flash,session
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
def home():
    return render_template('main_pages/index.html')

@app.route('/dashbord1')
def dashboard_admin():
    return render_template('base.html')


#Log out function
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('dashbord'))  # Redirect to the dashboard route



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
            return redirect(url_for('admin_dashbord'))  # Redirect to home on error

    return render_template('admin.html')  

@app.route('/admin_dashbord')
def admin_dashbord():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM stock")
    stock=cur.fetchall()
    return render_template('admin_dashbord.html',stock=stock)



@app.route('/add', methods=['GET','POST'])
def add_stock():
    if request.method == 'POST':
        item_name = request.form['item-name']
        quantity=request.form['quantity']
        price=request.form['price']
        reorder_level=request.form['reorder-level']
        cur=mysql.connection.cursor() #interact with DB
        cur.execute("INSERT INTO stock (item_name, quantity, price, reorder_level) VALUES (%s, %s, %s, %s)", (item_name, quantity, price, reorder_level))
        mysql.connection.commit() # save
        cur.close()  # Close the cursor
        return redirect(url_for('admin_dashbord'))
    return redirect(url_for('admin_dashbord'))

#stock update
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
        return redirect(url_for('admin_dashbord'))
    
    # If GET request, fetch the current stock data
    cur.execute("SELECT * FROM stock WHERE id = %s", (id,))
    stock = cur.fetchone()
    cur.close()
    return render_template('update_stock.html', stock=stock)

@app.route('/delete/<int:id>', methods=['GET'])
def delete_stock(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM stock WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('admin_dashbord'))

#about mainpage

#main page appoiment
@app.route('/about')
def about_main():

    return render_template(('main_pages/about.html'))

#main page docter page
@app.route('/doctor')
def doctor_main():

    return render_template('main_pages/doctors.html')

#main apge gallery
@app.route('/gallery')
def gallery_main():

    return render_template('main_pages/gallery.html')

#main page contact
@app.route('/contact')
def contact_main():

    return render_template('main_pages/contact.html')



#registration
@app.route('/register')
def register_main():

    return render_template(('main_pages/registration.html'))


#main home routing path
@app.route('/login')
def login_main():

    return render_template(('main_pages/login.html'))

#main page appoiment
@app.route('/booking')
def appoiment_main():

    return render_template(('main_pages/appointment.html'))








    




if __name__ == "__main__":
    app.run(debug=True)  


