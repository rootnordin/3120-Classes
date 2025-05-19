# Halo Reach Sci‑Fi Armory (Phase 2)

## Overview
Phase 2 upgrades the in-memory CLI armory system to use SQLite for persistent data storage. User accounts, items, borrow/return transactions, and credits are all stored in a local database file (`armory.db`).

## Requirements
- Python 3.7+ (with built-in `sqlite3` module)
- No external libraries required

## Repository Contents
- `main.py`: CLI script connecting to SQLite, implementing all game features.
- `armory.db`: SQLite database (created automatically on first run).
- `README.md`: This documentation.

## Database Schema
1. **users**
   - `id` INTEGER PRIMARY KEY
   - `name` TEXT UNIQUE
   - `credits` INTEGER
2. **items**
   - `id` INTEGER PRIMARY KEY
   - `name` TEXT UNIQUE
   - `available` INTEGER (0 = false, 1 = true)
3. **transactions**
   - `id` INTEGER PRIMARY KEY AUTOINCREMENT
   - `user_id` INTEGER REFERENCES users(id)
   - `item_id` INTEGER REFERENCES items(id)
   - `borrow_date` TEXT (ISO timestamp)
   - `return_date` TEXT (ISO timestamp or NULL until returned)

## Setup & Usage
1. **Clone & branch** (if not already):
   ```bash
   git clone git@github.com:rootnordin/3120-Classes.git
   cd 3120-Classes
   git checkout -b phase2-db