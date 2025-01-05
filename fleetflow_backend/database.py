# This module is all about database

import sqlite3, json

#connect database (if not exists)
def database():
    try:
        conn = sqlite3.connect('database.sqlite')
    except Exception as e:
        print('The Database cannot be connected due to: ' + e)
    return (conn)

#create a user table
def user_table():
    db = database()
    query = """CREATE TABLE IF NOT EXISTS user(
                id integer PRIMARY KEY,
                username text NOT NULL,
                email text NOT NULL UNIQUE,
                password text NOT NULL
                )
            """
    db.execute(query)
try:
    user_table()
except Exception as e:
    print('The table cannot be created due to: ' + e)

#write into the user table
def create_user(username, email, password):
    db = database()
    query = """INSERT INTO user(username, email, password) VALUES(?, ?, ?)"""
    db.execute(query, (username, email, password))
    db.commit()

def read_user():
    db = database()
    query = """SELECT * FROM user"""
    query_exe = db.execute(query)
    all_users = query_exe.fetchall()

    user_array = []

    for user in all_users:
        user_dic = {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'password': user[3]
        }
        user_array.append(user_dic)
    
    return (user_array)

