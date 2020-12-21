import sqlite3

def db_connection():
    with sqlite3.connect('dejirbot.db') as conn:
        return conn

def create_message_table():
    query = "CREATE TABLE IF NOT EXISTS message (id int, message text, label text, user_id int, is_approved bool, date text)"
    db_exec(query)

def insert_message(msg, msg_type):
    query = f"INSERT INTO message VALUES ('{msg.message_id}','{msg.text}','{msg_type}', '{msg.from_user.id}', null, '{msg.date}')"
    db_exec(query)
    

def db_exec(query):
    c = db_connection()
    c.cursor().execute(query)
    c.commit()
    c.close()

if __name__ == '__main__':
    create_message_table()