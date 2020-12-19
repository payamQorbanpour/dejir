import sqlite3

def db_connection():
    with sqlite3.connect('dejirbot.db') as conn:
        return conn