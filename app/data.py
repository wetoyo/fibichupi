import sqlite3
from datetime import datetime, timezone
from fetch_git import get_commits

DB_FILE = "database.db"

def _conn():
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    return db

def get_balance(user_id):
    db = _conn()
    row = db.execute("SELECT commits FROM user WHERE user_id = ?", (user_id,)).fetchone()
    db.close()
    return row["commits"] if row else 0

def get_user_bets(user_id):
    db = _conn()
    rows = db.execute(
        """SELECT b.*, m.title, m.status, m.result
           FROM bets b JOIN markets m ON m.id = b.market_id
           WHERE b.user_id = ? ORDER BY b.timestamp DESC""",
        (user_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]

def get_user_markets(user_id):
    db = _conn()
    rows = db.execute(
        "SELECT * FROM markets WHERE creator_id = ? ORDER BY id DESC",
        (user_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]

def get_market_totals(market_id):
    db = _conn()
    rows = db.execute(
        "SELECT side, COALESCE(SUM(amount), 0) AS total FROM bets WHERE market_id = ? GROUP BY side",
        (market_id,),
    ).fetchall()
    db.close()
    totals = {"yes": 0, "no": 0}
    for r in rows:
        totals[r["side"]] = r["total"]
    return totals

def current_price(market_id):
    t = get_market_totals(market_id)
    pool = t["yes"] + t["no"]
    if pool == 0:
        return 0.5
    return t["yes"] / pool

def get_market(market_id):
    db = _conn()
    row = db.execute("SELECT * FROM markets WHERE id = ?", (market_id,)).fetchone()
    db.close()
    return dict(row) if row else None

def get_price_history(market_id):
    db = _conn()
    rows = db.execute(
        "SELECT timestamp, price FROM price_history WHERE market_id = ? ORDER BY id ASC",
        (market_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]

def get_market_bets(market_id):
    db = _conn()
    rows = db.execute(
        "SELECT * FROM bets WHERE market_id = ? ORDER BY timestamp DESC",
        (market_id,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]

def get_all_markets():
    db = _conn()
    rows = db.execute("SELECT * FROM markets ORDER BY id DESC").fetchall()
    db.close()
    return [dict(r) for r in rows]

def place_bet(user_id, market_id, side, amount):
    if side not in ("yes", "no"):
        return "Invalid side."
    if amount <= 0:
        return "Amount must be positive."
    market = get_market(market_id)
    if not market:
        return "Market not found."
    if market["creator_id"] == user_id:
        return "You cannot bet on your own market."
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

def resolve_market(market_id, result, user_id):
    market = get_market(market_id)
    if not market:
        return "Market not found."
    if market["creator_id"] != user_id:
        return "Only the creator can resolve."
    if market["status"] != "open":
        return "Market already resolved."
    if result not in ("yes", "no"):
        return "Invalid result."

    totals = get_market_totals(market_id)
    pool = totals["yes"] + totals["no"]
    winner_pool = totals[result]

    db = _conn()
    if winner_pool > 0:
        winners = db.execute(
            "SELECT user_id, SUM(amount) AS staked FROM bets WHERE market_id = ? AND side = ? GROUP BY user_id",
            (market_id, result),
        ).fetchall()
        for w in winners:
            payout = int(round(pool * (w["staked"] / winner_pool)))
            db.execute("UPDATE user SET commits = commits + ? WHERE user_id = ?",
                       (payout, w["user_id"]))
    db.execute("UPDATE markets SET status = 'resolved', result = ? WHERE id = ?",
               (result, market_id))
    db.commit()
    db.close()
    return "ok"

def update_commits(user_id):
    db = _conn()
    row = db.execute("SELECT lastcomm FROM user WHERE user_id = ?", (user_id,)).fetchone()
    since = None
    if row and row["lastcomm"]:
        since = datetime.strptime(row["lastcomm"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    coms, date = get_commits(user_id, since)
    if coms != 0:
        db.execute("UPDATE user SET commits = commits + ?, lastcomm = ? WHERE user_id = ?",
                   (coms, date, user_id))
        db.commit()
    db.close()
