import sqlite3

class User:
    
    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email
        
    def create_user(self, username, password, email):
        
        self.username = username
        self.password = password
        self.email = email
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f""" SELECT password FROM users WHERE Username = '{self.username}'; """)
        exist = cursor.fetchone()

        if exist is None:
            cursor.execute(f""" INSERT INTO users(username, password, email) VALUES ('{self.username}', '{self.password}', '{self.email}'); """)

            connection.commit()
            cursor.close()
            connection.close()

        else:
            return ('User already exist!!!')

        return 'You have signed up, successfully!!!'

    def check_users(self):
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(""" SELECT username FROM users ORDER BY id DESC; """)
        db_users = cursor.fetchall()
        users = [db_users[i][0] for i in range(len(db_users))]

        connection.commit()
        cursor.close()
        connection.close()

        return users


    def check_password(self, username):
        self.username = username
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f""" SELECT password FROM users WHERE username = '{self.username}' ORDER BY id DESC; """)
        password = cursor.fetchone()[0]

        connection.commit()
        cursor.close()
        connection.close()

        return password

user = User()

class Task:
    
    def create_task(self, title, description, status, creator):
        
        self.title = title
        self.description = description
        self.status = status 
        self.creator = creator
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f""" SELECT title FROM tasks WHERE title = '{self.title}'; """)
        task_exist = cursor.fetchone()

        if task_exist is None:
            cursor.execute(f""" INSERT INTO tasks(title, description, status, creator) VALUES ('{self.title}', '{self.description}', '{self.status}', '{self.creator}'); """)

            connection.commit()
            cursor.close()
            connection.close()
        else:
            return 'Task already exist'

        return 'Task created, successfully!'

    def retrieve_tasks(self, creator):
        
        self.creator = creator 
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(f""" SELECT * FROM tasks WHERE creator = '{self.creator}' ; """)
        tasks = cursor.fetchall()

        connection.commit()
        cursor.close()
        connection.close()

        return tasks

    def edit_task(self, id):
        
        self.id = id
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(f""" SELECT title, description FROM tasks WHERE id = '{self.id}'; """)
        task = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

        return task

    def update_task(self, id, title, description, status):
        
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        cursor = connection.cursor()    
        cursor.execute(f""" UPDATE tasks SET title = '{self.title}', description = '{self.description}', status = '{self.status}' WHERE id = '{self.id}'; """ )

        connection.commit()
        cursor.close()
        connection.close()

    def delete_task(self, id):
        
        self.id = id
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f""" DELETE FROM tasks WHERE id = '{self.id}'; """)

        connection.commit()
        cursor.close()
        connection.close()

        return 'Task deleted, successfully!'

task = Task()

class Admin:
    
    def get_all_users(self):
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(""" SELECT * FROM users ORDER BY id DESC; """)
        db_users = cursor.fetchall()

        connection.commit()
        cursor.close()
        connection.close()

        return db_users
    
    def get_all_tasks(self):
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(""" SELECT * FROM tasks ORDER BY id DESC; """)
        tasks = cursor.fetchall()
        all_tasks = len(tasks)

        connection.commit()
        cursor.close()
        connection.close()

        return all_tasks
    
    def get_last_24hrs_users(self):
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE "when" >= date('now', '-1 days') AND "when" < date('now'); """)
        one_day_old_users = cursor.fetchall()
        signups = len(one_day_old_users)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return signups
    
    def get_last_24hrs_tasks(self):
        
        connection = sqlite3.connect('todo_app.db', check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM tasks WHERE "when" >= date('now', '-1 days') AND "when" < date('now'); """)
        one_day_old_tasks = cursor.fetchall()
        result = len(one_day_old_tasks)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return result
    
        
    
    
admin = Admin()

