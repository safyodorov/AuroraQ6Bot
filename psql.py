import psycopg2
import os

# база данных телеграм пользователей
DB_URI = os.environ['DATABASE_URL']
db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

def get_user():
# запрашиваю из базы данных список юзеров
    db_object.execute(f"SELECT id FROM users WHERE qset = 5")
    joinedUser5 = db_object.fetchone()
    db_object.execute(f"SELECT id FROM users WHERE qset = 6")
    joinedUser6 = db_object.fetchone()
    db_object.execute(f"SELECT id FROM users WHERE qset = 7")
    joinedUser7 = db_object.fetchone()
    db_object.execute(f"SELECT id FROM users WHERE qset = 8")
    joinedUser8 = db_object.fetchone()
    db_object.execute(f"SELECT id FROM users WHERE qset = 9")
    joinedUser9 = db_object.fetchone()
    return (joinedUser5, joinedUser6, joinedUser7, joinedUser8, joinedUser9)

def id_check(id, username):
    db_object.execute(f"SELECT id FROM users WHERE id = {id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO users(id, username, qset) VALUES(%s, %s, %s)", (id, username, 0))
        db_connection.commit()

def id_write(id, data):
    db_object.execute(f"UPDATE users SET qset = {data} WHERE id = {id}")
    db_connection.commit()