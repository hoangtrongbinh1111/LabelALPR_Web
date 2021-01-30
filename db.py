import sqlite3
from flask import current_app,g
conn = sqlite3.connect('database.db')
print ("Opened database successfully")

# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
conn.execute('CREATE TABLE Plate (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,image_name TEXT NOT NULL,labelPlate TEXT NOT NULL)')
print ("Table created successfully")
conn.close()