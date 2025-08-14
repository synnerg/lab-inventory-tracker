import sqlite3, pandas as pd, pathlib

db = sqlite3.connect("inventory.db")
cur = db.cursor()

# 1. create tables
cur.executescript("""
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS UsageLog;

CREATE TABLE Inventory(
  item_id TEXT PRIMARY KEY,
  item_name TEXT,
  category TEXT,
  quantity REAL,
  unit TEXT,
  reorder_threshold REAL,
  location TEXT,
  notes TEXT
);

CREATE TABLE UsageLog(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT,
  item_id TEXT,
  amount_used REAL,
  unit TEXT,
  by_whom TEXT,
  reason TEXT
);
""")

# 2. import CSVs (if they exist)
if pathlib.Path("inventory.csv").exists():
    df = pd.read_csv("inventory.csv")
    df.to_sql("Inventory", db, if_exists="append", index=False)

if pathlib.Path("usage_log.csv").exists():
    df = pd.read_csv("usage_log.csv")
    df.rename(columns={"by":"by_whom"}, inplace=True)
    df.to_sql("UsageLog", db, if_exists="append", index=False)

db.commit()
db.close()
print("inventory.db created & populated.")
