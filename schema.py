import sqlite3

connection = sqlite3.connect('todo_app.db', check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
    """ CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(24),
        password VARCHAR(32),
        email VARCHAR(55)
    ); """
)

cursor.execute(
    """CREATE TABLE tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title CHAR(50),
        description VARCHAR(255),
        status DEFAULT 0,
        creator VARCHAR(24),
        FOREIGN KEY(creator) REFERENCES users(username)
    ); """
)

cursor.execute(
    """ CREATE TABLE administrators(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(24),
        password VARCHAR(32)
    ); """
)

print("Tables created successfully")

connection.commit()
cursor.close()
connection.close()

        # username VARCHAR(24),
        # FOREIGN KEY(username) REFERENCES users(username)

