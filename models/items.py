from flask_mysqldb import MySQL

mysql=None

def get_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    cur.close()
    return rows