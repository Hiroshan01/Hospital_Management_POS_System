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