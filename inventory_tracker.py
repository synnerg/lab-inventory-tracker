import argparse
from pathlib import Path
import pandas as pd


INV_PATH = Path("inventory.csv")
USAGE_PATH = Path("usage_log.csv")
RESTOCK_PATH = Path("restock_list.csv")

# Load inventory from CSV
def load_inventory():
    if not INV_PATH.exists():
        raise FileNotFoundError("inventory.csv not found")
    return pd.read_csv(INV_PATH)

# Load usage log
def load_usage():
    if not USAGE_PATH.exists():
        cols = ["timestamp","item_id","amount_used","unit","by","reason"]
        return pd.DataFrame(columns=cols)
    return pd.read_csv(USAGE_PATH)

# Print inventory 
def show_status():
    df = load_inventory()
    print("\nCurrent lab inventory:\n")
    print(df.to_markdown(index=False))

# Apply usage to inventory
def apply_usage():
    inv = load_inventory().set_index("item_id")
    usage = load_usage()

    if usage.empty:
        print("No rows in usage_log.csv – nothing to apply")
        return

    for _, row in usage.iterrows():
        iid = row["item_id"]
        used = float(row["amount_used"])
        if iid in inv.index:
            new_qty = max(0, inv.at[iid, "quantity"] - used)
            inv.at[iid, "quantity"] = new_qty
        else:
            print(f"Warning: {iid} in usage log but not in inventory")

    inv.reset_index().to_csv(INV_PATH, index=False)
    print("Usage applied. inventory.csv updated.")

# Generate a restock list
def make_restock_list():
    inv = load_inventory()
    need = inv[inv["quantity"] <= inv["reorder_threshold"]]
    if need.empty:
        print("All items above threshold. No restock needed.")
    else:
        need.to_csv(RESTOCK_PATH, index=False)
        print(f"restock_list.csv created with {len(need)} items")

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Lab Inventory Tracker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show current inventory")
    sub.add_parser("apply-usage", help="Apply usage_log.csv to inventory")
    sub.add_parser("restock", help="Create restock_list.csv for low stock items")

    args = parser.parse_args()

    if args.cmd == "status":
        show_status()
    elif args.cmd == "apply-usage":
        apply_usage()
    elif args.cmd == "restock":
        make_restock_list()

if __name__ == "__main__":
    main()
