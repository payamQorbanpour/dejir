def upgrade(connection):
    connection.execute('''CREATE TABLE message (id int, message text, label text, user_id int, is_approved bool, date text)''')
    connection.commit()

def downgrade(connection):
    connection.execute('drop table animals')