import hashlib
import sqlite3
import json
import time
from datetime import datetime


ONLINE_LAST_MINUTES = 5

def mark_online(user_id):
    now = int(time.time())
    expires = now + (app.config['ONLINE_LAST_MINUTES'] * 60) + 10
    all_users_key = 'online-users/%d' % (now // 60)
    user_key = 'user-activity/%s' % user_id
    p = redis.pipeline()
    p.sadd(all_users_key, user_id)
    p.set(user_key, now)
    p.expireat(all_users_key, expires)
    p.expireat(user_key, expires)
    p.execute()

def get_user_last_activity(user_id):
    last_active = redis.get('user-activity/%s' % user_id)
    if last_active is None:
        return None
    return datetime.utcfromtimestamp(int(last_active))

def get_online_users():
    current = int(time.time()) // 60
    minutes = xrange(app.config['ONLINE_LAST_MINUTES'])
    return redis.sunion(['online-users/%d' % (current - x)
                         for x in minutes])

def passwordHasher(password):

    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def checkIfUserExists(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
    data = cursor.fetchone()
    if data is None:
        print(' There is NO user with username:  %s' % username)
        return False
    else:
        print(' User FOUND for username %s' % username)
        return True


def registerUser(username, password):
    conn = sqlite3.connect('users.db')
    conn.execute("INSERT INTO USERS (USERNAME,PASSWORD) VALUES (?, ?)", (username, password));
    conn.commit()


def loginUserCheck(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT PASSWORD FROM USERS WHERE USERNAME = ?", (username,))
    data = cursor.fetchone()
    print(data)
    print(password)
    if data[0] == password:
        print('True creds')
        return True
    else:
        print('False creds')
        return False


def returnUsernamesFromDb():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT USERNAME FROM USERS")
    data = cursor.fetchone()
    return data

def returnUrlsOnly(urlPool):
    pool = []
    for item in urlPool:
        item = json.loads(item)
        pool.append(item["url"])

    return pool





