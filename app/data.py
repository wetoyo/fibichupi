import sqlite3
from fetch_git import get_commits

DB_FILE = "database.db"

def create_bet(id, user_id, market_id, side, amount, timestamp):
    try:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        command = "INSERT INTO bets VALUES (?, ?, ?, ?, ?, ?)"
        vars = (id, user_id, market_id, side, amount, timestamp)
        c.execute(command, vars)

        db.commit()
        db.close()

        return f"bet_id {id} created"
    except sqlite3.Error as e:
        print(f"SQLite error in create_bet(): {e}")

def create_market(id, title, description, creator_id, status, result):
    try:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        command = "INSERT INTO markets VALUES (?, ?, ?, ?, ?, ?)"
        vars = (id, title, description, creator_id, status, result)
        c.execute(command, vars)

        db.commit()
        db.close()

        return f"market_id {id} created"
    except sqlite3.Error as e:
        print(f"SQLite error in create_market(): {e}")

def get_market_bets(market_id):
    try:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        command = "SELECT side, amount FROM bets WHERE market_id = ?"
        vars = (market_id,)
        results = c.execute(command, vars).fetchall()

        db.close()

        return results
    except sqlite3.Error as e:
        print(f"SQLite error in get_market_bets(): {e}")

def get_market_price(market_id, timestamp):
    try:
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        command = "SELECT price FROM price_history WHERE market_id = ? AND timestamp = ?"
        vars = (market_id, timestamp)
        results = c.execute(command, vars).fetchall()

        db.close()

        return results
    except sqlite3.Error as e:
        print(f"SQLite error in get_market_price(): {e}")

def update_commits(user_id):
    try:
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
    except sqlite3.Error as e:
        print(f"SQLite error in update_commits(): {e}")
        return f"failed to update commits for {user_id}"

def get_user_bets():
    return 0

def get_user_markets():
    return 0
