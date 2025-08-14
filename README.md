# 🧪 Lab Inventory Tracker

This is a command-line tool for tracking lab inventory, applying usage logs, and generating restock lists. Built in Python using `pandas`.

## 🔧 Features

- View current lab inventory as a clean table
- Apply usage logs from CSV (e.g., experiment consumption)
- Automatically generate `restock_list.csv` when stock is low
- Simple CLI using `argparse`
- Clean, readable pandas-powered CSV logic

## 🛠️ How to Use

```bash
python inventory_tracker.py status
python inventory_tracker.py apply-usage
python inventory_tracker.py restock
