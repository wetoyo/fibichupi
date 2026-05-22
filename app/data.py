import sqlite3
from fetch_git import get_commits

DB_FILE = "database.db"

def _conn():
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    return db

def currentprice(market_id):
    pass

def get_market(market_id):
    pass

def get_balance(user_id):
    pass

def get_commits(user_id):
    pass

def place_bet(user_id, market_id, side, amount):
    if side not in ("yes", "no"):
        return "Invalid side."
    if amount <= 0:
        return "Amount must be positive."
    market = get_market(market_id)
    if not market:
        return "Market not found."
    if market["status"] != "open":
        return "Market is closed."
    if get_balance(user_id) < amount:
        return "Not enough commits."

    db = _conn()
    db.execute("UPDATE user SET commits = commits - ? WHERE user_id = ?", (amount, user_id))
    db.execute(
        "INSERT INTO bets (user_id, market_id, side, amount, timestamp) VALUES (?, ?, ?, ?, ?)",
        (user_id, market_id, side, amount, datetime.utcnow().isoformat()),
    )
    db.commit()
    db.close()

    price = current_price(market_id)
    db = _conn()
    db.execute(
        "INSERT INTO price_history (market_id, timestamp, price) VALUES (?, ?, ?)",
        (market_id, datetime.utcnow().isoformat(), price),
    )
    db.commit()
    db.close()
    return "ok"

def create_market(title, description, creator_id):
    db = _conn()
    c = db.execute(
        "INSERT INTO markets (title, description, creator_id, status, result) VALUES (?, ?, ?, 'open', NULL)",
        (title, description, creator_id),
    )
    market_id = c.lastrowid
    # seed price history at 0.5
    db.execute(
        "INSERT INTO price_history (market_id, timestamp, price) VALUES (?, ?, ?)",
        (market_id, datetime.utcnow().isoformat(), 0.5),
    )
    db.commit()
    db.close()
    return market_id

def get_market_bets(market_id):
    db = _conn()
    rows = db.execute(
        "SELECT * FROM bets WHERE market_id = ? ORDER BY timestamp DESC",
        (market_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]

def update_commits(user_id):
    coms, date = get_commits(user_id)
    db = _conn()
    db.execute("UPDATE user SET commits = commits + ?, lastcomm = ? WHERE user_id = ?",
               (coms, date, user_id))
    db.commit()
    db.close()

def get_user_bets():
    return 0

def get_user_markets():
    return 0
