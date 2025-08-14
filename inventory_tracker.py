import argparse, sqlite3, pandas as pd
from pathlib import Path
from tabulate import tabulate

DB_PATH = Path("inventory.db")

# ---------- helpers ----------
def db():
    return sqlite3.connect(DB_PATH)

def show_status():
    with db() as conn:
        df = pd.read_sql("SELECT * FROM Inventory", conn)
    print("\nCurrent lab inventory:\n")
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))

def apply_usage():
    with db() as conn:
        usage = pd.read_sql("SELECT * FROM UsageLog", conn)
        if usage.empty:
            print("No rows in UsageLog – nothing to apply")
            return

        cur = conn.cursor()
        for _, row in usage.iterrows():
            cur.execute("""
              UPDATE Inventory
                 SET quantity = MAX(quantity - ?, 0)
               WHERE item_id = ?;
            """, (row["amount_used"], row["item_id"]))
        conn.commit()
    print("Usage applied. Inventory updated.")

def make_restock_list():
    with db() as conn:
        df = pd.read_sql("""
          SELECT *
            FROM Inventory
           WHERE quantity <= reorder_threshold
        """, conn)
    if df.empty:
        print("All items above threshold. No restock needed.")
    else:
        df.to_csv("restock_list.csv", index=False)
        print(f"restock_list.csv created with {len(df)} items")

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Lab Inventory Tracker (SQLite)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("apply-usage")
    sub.add_parser("restock")
    args = parser.parse_args()

    if args.cmd == "status":
        show_status()
    elif args.cmd == "apply-usage":
        apply_usage()
    elif args.cmd == "restock":
        make_restock_list()

if __name__ == "__main__":
    if not DB_PATH.exists():
        print("❌ inventory.db not found — run the setup script first.")
    else:
        main()
