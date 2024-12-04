from flask_mysqldb import MySQL

mysql=None

from flask_mysqldb import MySQL

class UserData:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def get_users(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM users_data")
        return cursor.fetchall()
 
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

