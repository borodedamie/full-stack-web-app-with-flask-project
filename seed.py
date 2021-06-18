import sqlite3

connection = sqlite3.connect('todo_app.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """INSERT INTO tasks(title, description, status) VALUES ('Create DB', 'create tables for the todo application', 0 );"""
)

cursor.execute(
    """INSERT INTO tasks(title, description, status) VALUES ('Code the task CRUD', 'using functional programming, code out the functions for the to do application', 0 );"""
)

connection.commit()
cursor.close()
connection.close()

