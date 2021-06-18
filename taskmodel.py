import sqlite3

def create_task(title, description, status, creator):
    connection = sqlite3.connect('todo_app.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(f""" SELECT title FROM tasks WHERE title = '{title}'; """)
    task_exist = cursor.fetchone()

    if task_exist is None:
        cursor.execute(""" INSERT INTO tasks(title, description, status, creator) VALUES ('{title}', '{description}', '{status}', '{creator}'); """.format(title = title, description = description, status = status, creator = creator))

        connection.commit()
        cursor.close()
        connection.close()
    else:
        return 'Task already exist'

    return 'Task created, successfully!'

def retrieve_tasks(creator):
    connection = sqlite3.connect('todo_app.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(f""" SELECT * FROM tasks WHERE creator = '{creator}' ; """)
    tasks = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return tasks

def edit_task(id):
    connection = sqlite3.connect('todo_app.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(f""" SELECT title, description FROM tasks WHERE id = '{id}'; """)
    task = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return task

def update_task(id, title, description, status):
    connection = sqlite3.connect('todo_app.db', check_same_thread=False)
    cursor = connection.cursor()    
    cursor.execute(f""" UPDATE tasks SET title = '{title}', description = '{description}', status = '{status}' WHERE id = '{id}'; """ )

    connection.commit()
    cursor.close()
    connection.close()

def delete_task(id):
    connection = sqlite3.connect('todo_app.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(f""" DELETE FROM tasks WHERE id = '{id}'; """)

    connection.commit()
    cursor.close()
    connection.close()

    return 'Task deleted, successfully!'

