# Stock Update Route
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_stock(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        item_name = request.form['item-name']
        quantity = request.form['quantity']
        price = request.form['price']
        reorder_level = request.form['reorder-level']
        
       
        cur.execute("""
            UPDATE stock 
            SET item_name = %s, quantity = %s, price = %s, reorder_level = %s 
            WHERE id = %s""", (item_name, quantity, price, reorder_level, id))
        
        mysql.connection.commit() 
        cur.close()  
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