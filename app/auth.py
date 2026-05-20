##placeholder from p0
import sqlite3
import random
import fetch_git
DB_FILE = "database.db"
def create_tbs():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS user(user_id TEXT PRIMARY KEY, password TEXT, commits INTEGER, lastcomm TEXT)")
    db.commit()
    db.close()
create_tbs()
#checks if username already in db
def user_exists(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM user WHERE user_id = ?", (username,))
    result = c.fetchone() != None
    db.close()
    return result

#checks if username input has special characters besides _
def user_valid(username):
    for charac in username:
        if not (charac.isalnum() or charac == "_"):
            return False
    return True

#checks if password input matches password in db
def login(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT password FROM user where user_id = ?", (username,))
    pw = c.fetchone()[0]
    db.close()
    return pw == password

#checks if username is taken, is valid, and adds username and password input to db
def register(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if (username.strip() == "" or password.strip() == ""):
        db.close()
        return "Username or password cannot be empty."
    if not user_valid(username):
        db.close()
        return "Username cannot have special characters except '_'."
    if user_exists(username):
        db.close()
        return "Username is already taken."
    coms, date = fetch_git.get_commits(username)
    c.execute("INSERT INTO user (user_id, password, commits, lastcomm) VALUES (?, ?, ?, ?)", (username, password, coms, date))
    db.commit()
    db.close()
    return "Registered"

#deletes account
def delete_acc(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM user WHERE user_id = ?", (username,))
    db.commit()
    db.close()
