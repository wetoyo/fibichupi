import sqlite3
from fetch_git import get_commits

DB_FILE = "database.db"


def create_bet(id, user_id, market_id, side, amount, timestamp):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = "INSERT INTO bets VALUES (?, ?, ?, ?, ?, ?)"
    vars = (id, user_id, market_id, side, amount, timestamp)
    c.execute(command, vars)

    db.commit()
    db.close()

    return f"bet_id {id} created"

def create_market(id, title, description, creator_id, status, result):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = "INSERT INTO bets VALUES (?, ?, ?, ?, ?, ?)"
    vars = (id, title, description, creator_id, status, result)
    c.execute(command, vars)

    db.commit()
    db.close()

    return f"market_id {id} created"

def update_commits(user_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = "UPDATE user SET commits = commits + ? WHERE user_id = ?"
    coms, date = get_commits(user_id)
    vars = (coms, user_id)
    c.execute(command, vars)
    
    command = "UPDATE user SET lastcomm = ? WHERE user_id = ?"
    vars = (date, user_id)
    c.execute(command, vars)

    db.commit()
    db.close()

    return f"commit amount for {user_id} updated"
