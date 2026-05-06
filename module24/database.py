import sqlite3

connection = sqlite3.connect("example.db")


cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    position TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL
    )

''')

connection.commit()

cursor.execute('''
INSERT INTO employees(name, position, department, salary)
VALUES(?,?,?,?)
''' , ("Gerti", "Software Engineer", "IT", 120000))
connection.commit()
cursor.execute("Select * From employees")