import sqlite3

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.executescript("""
    DROP TABLE IF EXISTS markets;
    CREATE TABLE markets (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        creator_id INTEGER,
        status TEXT,
        result TEXT
    );
    DROP TABLE IF EXISTS bets;
    CREATE TABLE bets (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        market_id INTEGER,
        side TEXT,
        amount INTEGER,
        timestamp DATETIME
    );
    DROP TABLE IF EXISTS price_history;
    CREATE TABLE price_history (
        id INTEGER PRIMARY KEY,
        market_id INTEGER,
        timestamp DATETIME,
        price REAL
    );
""")

db.commit()
db.close()
