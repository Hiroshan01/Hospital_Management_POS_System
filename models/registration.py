import mysql.connector
from flask import request

def register_user(db_connection):
      if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email=request.form['email']
        password=request.form['password']
       
        cur=mysql.connection.cursor() #interact with DB
        cur.execute("INSERT INTO registration (first_name, last_name, 	email, password) VALUES (%s, %s, %s, %s)", (first_name,  last_name, email, ))
        mysql.connection.commit() # save
        cur.close()  # Close the cursor
      


