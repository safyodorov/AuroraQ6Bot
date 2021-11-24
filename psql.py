import psycopg2
import os

# база данных телеграм пользователей
DB_URI = os.environ['DATABASE_URL']
db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

def get_users():
# запрашиваю из базы данных список юзеров
    joinedUsers = []
    for i in range(5, 10):
        db_object.execute(f"SELECT id FROM users WHERE qset = {i}")
        joinedUsers[i-4] = db_object.fetchone()
    return (joinedUsers)

def id_check(id, username):
    db_object.execute(f"SELECT id FROM users WHERE id = {id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO users(id, username, qset) VALUES(%s, %s, %s)", (id, username, 0))
        db_connection.commit()

def id_write(id, data):
    db_object.execute(f"UPDATE users SET qset = {data} WHERE id = {id}")
    db_connection.commit()