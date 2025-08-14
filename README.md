# 🧪 Lab Inventory Tracker (SQLite + Python)

This is a command-line inventory tracker I built to manage lab stock efficiently. It uses a local SQLite database (`inventory.db`) and lets you:

- Track and view current lab items
- Apply usage logs (e.g., experiment consumption)
- Auto-generate a restock list
- Keep everything clean with `pandas` + `tabulate`

No web UI — just clean, readable CLI and local data handling.

---

## 🔧 Features

- 📦 View lab inventory in a grid-style table
- 📉 Apply usage logs to update quantities
- 📋 Generate `restock_list.csv` for items below threshold
- 🧠 Simple, no-nonsense CLI (`argparse`)
- 🗂️ Local storage using SQLite (no server needed)

---

## ⚙️ Setup

1. Install dependencies:

```bash
pip install pandas tabulate
