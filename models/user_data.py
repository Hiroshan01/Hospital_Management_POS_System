from flask_mysqldb import MySQL

mysql=None
#sele
'''''
#insert user
# add_user.py
def add_user(data):
    user_name = data['user_name']
    address = data['address']
    phone_no = data['phone_no']
    comment = data.get('comment', '') 

    # Insert into database
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO users_data (user_name, address, phone_no, comment) 
        VALUES (%s, %s, %s, %s)
    """, (user_name, address, phone_no, comment))
    mysql.connection.commit()
    cur.close()
    
    return 
'''


#Function to retrive a
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users_data")
    rows = cur.fetchall()
    cur.close()
    return rows
 
# Function to update user
def update_user(user_id, data):
    user_name = data.get('user_name')
    address = data.get('address')
    phone_no = data.get('phone_no')
    comment = data.get('comment', '')
    
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE users_data 
        SET user_name = %s, address = %s, phone_no = %s, comment = %s 
        WHERE user_id = %s
    """, (user_name, address, phone_no, comment, user_id))
    mysql.connection.commit()
    cur.close()
    return {"message": "User updated successfully"}

#delete user
def delete_user(user_id):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM users_data WHERE user_id = %s", [user_id])
    mysql.connection.commit()
    cur.close()
    return {"message": "User deleted successfully"}

