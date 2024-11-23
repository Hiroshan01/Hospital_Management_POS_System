import mysql.connector
from flask import request

def register_user(mysql):
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        
        # Interact with the database
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO registration (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, password)
            )
            mysql.connection.commit()  # Save the changes
            cur.close()  # Close the cursor
            return "Registration successful!"
        except Exception as e:
            return f"An error occurred: {e}"
