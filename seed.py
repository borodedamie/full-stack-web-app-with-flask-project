import sqlite3

connection = sqlite3.connect('todo_app.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """INSERT INTO administrators(username, password) VALUES ( 'admin', '1234Pa55w0rd' );"""
)

connection.commit()
cursor.close()
connection.close()

