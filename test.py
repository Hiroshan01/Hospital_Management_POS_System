 if request.method == 'POST':
        item_name = request.form['item_name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        reorder_level = int(request.form['reorder_level'])

        # Insert new stock item into the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO stock (item_name, quantity, price, reorder_level) VALUES (%s, %s, %s, %s)',
                       (item_name, quantity, price, reorder_level))
        mysql.connection.commit()
        cursor.close()
        return redirect('/stock')

    # Retrieve all stock items from the database
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM stock')
    stock_items = cursor.fetchall()
    cursor.close()


<a href="{{ url_for('delete_stock', id=stocks[0]) }}" class="btn btn-danger btn-sm">Delete</a>

#Log out function
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('dashbord'))  # Redirect to the dashboard route


#-----------------------------------------Admin credintial----------------------------#
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
#-----------------------------------------Admin credintial End----------------------------#


@app.route('/admin_dashbord_show_details')
def admin_dashbord():
    # Fetch booking details
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM booking")
    booking = cur.fetchall()
    
    # Fetch stock details
    cur.execute("SELECT * FROM stock")
    stock = cur.fetchall()
    cur.close()
    
    return render_template('admin_dashbord.html', booking=booking, stock=stock)



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
    return redirect(url_for(' admin_dashbord'))

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
#<-------------------------------Main Page Configuration Part----------------------------------->#
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

#main pager registration
@app.route('/registration')
def register_main():

    return render_template('main_pages/registration.html')




#registration
@app.route('/registerDB', methods=['GET', 'POST'])
def register_DB():
    if request.method == 'POST':

            first_name = request.form['first-name']
            last_name = request.form['last-name']
            email=request.form['email']
            password=request.form['password']    
            cur=mysql.connection.cursor() #interact with DB
            cur.execute("INSERT INTO registration (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (first_name,  last_name, email,password ))
            mysql.connection.commit() # save
            cur.close()  # Close the cursor
            return redirect(url_for('register_main'))
    return redirect(url_for('register_main'))

#main home routing path
@app.route('/login')
def login_main():

    return render_template(('main_pages/login.html'))

#main page appoiment
@app.route('/booking')
def appoiment_main():

    return render_template(('main_pages/appointment.html'))

#main page appoiment
@app.route('/bookingDB' , methods=['GET', 'POST'])
def appoiment_DB():
    if request.method == 'POST':
           
        name=request.form['name']
        email=request.form['email']
        purpose=request.form['subject']
        tel_No=request.form['number']
        department = request.form['department']
        date=request.form['date']
        time=request.form['Time']
        cur=mysql.connection.cursor() #interact with DB
        cur.execute("INSERT INTO booking(name, email, purpose, mobile_number, department,appointment_date, appointment_time) VALUES (%s, %s, %s, %s, %s, %s, %s)", ( name, email, purpose, tel_No , department , date , time ))
        mysql.connection.commit() # save
        cur.close() 
        return redirect(url_for('login_main'))
    return redirect(url_for('register_main'))

#---------------------User role --------------------------#
@app.route('/user_roles_login')
def user_role_login():
    
    return render_template('login_RBAC.html')

<a href="{{ url_for('delete_user', id=user[0]) }}" class="btn btn-danger btn-sm">Delete</a>
                            </td>







@app.route('/update_item/<int:id>', methods=['GET', 'POST'])
def update_items(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        item_name= request.form['item_name']
        company_name = request.form['company_name']
        dose=request.form['dose']
        genetic_name = request.form['genetic_name']
        brand_name = request.form['brand_name']
        specific1= request.form['specific1']

        # Update user details in the database
        try:
            cur.execute("""
                UPDATE items 
                SET item_name = %s, company_name = %s, dose = %s, genetic_name = %s , brand_name= %s ,specific1 = %s 
                WHERE id = %s
            """, (item_name, company_name, dose, genetic_name,brand_name ,specific1,id))
            mysql.connection.commit()
            return redirect(url_for('view_users'))  # Redirect after updating
        except Exception as e:
            print("Error updating user:", e)
            mysql.connection.rollback()  # Rollback if there's an error

    # Fetch user details for the GET request
    cur.execute("SELECT * FROM items  WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()

    return render_template('user/update_items.html', user=user)