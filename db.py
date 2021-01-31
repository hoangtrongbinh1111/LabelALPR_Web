import sqlite3
from flask import current_app,g
conn = sqlite3.connect('database.db')
print ("Opened database successfully")

# conn.execute('CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL)')
conn.execute("create table dataset_img (id INTEGER PRIMARY KEY AUTOINCREMENT,filename TEXT UNIQUE NOT NULL,label TEXT,status INT DEFAULT 0 NOT NULL,username TEXT  )")
#cur.execute("select * from Plate where username='Binh'")
#conn.execute('Drop table dataset_img')
#conn.execute('CREATE TABLE Plate (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,image_name TEXT NOT NULL,labelPlate TEXT NOT NULL)')
print ("Table created successfully")
conn.close()