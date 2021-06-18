import sqlite3

def create_user(username, password, email):
    connection = sqlite3.connect('todo_app.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(f""" SELECT password FROM users WHERE Username = '{username}'; """)
    exist = cursor.fetchone()

    if exist is None:
        cursor.execute(f""" INSERT INTO users(username, password, email) VALUES ('{username}', '{password}', '{email}'); """)

        connection.commit()
        cursor.close()
        connection.close()

    else:
        return ('User already exist!!!')

    return 'You have signed up, successfully!!!'

def check_users():
    connection = sqlite3.connect('todo_app.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username FROM users ORDER BY id DESC; """)
    db_users = cursor.fetchall()
    users = [db_users[i][0] for i in range(len(db_users))]

    connection.commit()
    cursor.close()
    connection.close()

    return users


def check_password(username):
    connection = sqlite3.connect('todo_app.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(f""" SELECT password FROM users WHERE username = '{username}' ORDER BY id DESC; """)
    password = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return password

