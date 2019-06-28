import hashlib
import sqlite3
import json



def passwordHasher(password):

    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def authenticateUser(username, password):
    return checkIfUserExists(username) and loginUserCheck(username, password)


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


def returnUsersOnly(urlPool):
    pool = []
    for item in urlPool:
        item = json.loads(item)
        pool.append(item["user"])

    return pool





