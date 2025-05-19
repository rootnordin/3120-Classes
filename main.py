
---

### main.py
```python
#!/usr/bin/env python3
"""
main.py: Halo Reach Sci‑Fi Armory Phase 2
Persistent in SQLite database with CLI interaction.
"""
import sqlite3
import os
from datetime import datetime

DB_FILE = 'armory.db'
DATE_FMT = '%Y-%m-%d %H:%M:%S'

class GameManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                credits INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                available INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                item_id INTEGER,
                borrow_date TEXT,
                return_date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(item_id) REFERENCES items(id)
            )
        ''')
        self.conn.commit()
        # Seed initial data if empty
        self.seed_users(['Noble Six', 'Kat', 'Carter', 'Jun'])
        self.seed_items(['Assault Rifle', 'Magnum Sidearm', 'Sniper Rifle', 'Frag Grenade', 'Jet Pack'])

    def seed_users(self, names):
        for name in names:
            self.cursor.execute(
                'INSERT OR IGNORE INTO users (name, credits) VALUES (?, ?)',
                (name, 100)
            )
        self.conn.commit()

    def seed_items(self, names):
        for name in names:
            self.cursor.execute(
                'INSERT OR IGNORE INTO items (name, available) VALUES (?, 1)',
                (name,)
            )
        self.conn.commit()

    def list_items(self):
        items = self.cursor.execute(
            'SELECT id, name FROM items WHERE available=1'
        ).fetchall()
        print("\nAvailable items:")
        for row in items:
            print(f"{row['id']}: {row['name']}")
        print()

    def borrow_item(self, user_id, item_id):
        # Check availability
        row = self.cursor.execute(
            'SELECT available FROM items WHERE id=?', (item_id,)
        ).fetchone()
        if not row:
            print("Invalid item ID.")
            return
        if row['available'] == 0:
            print("Item is not available.")
            return
        now = datetime.now().strftime(DATE_FMT)
        # Record transaction
        self.cursor.execute(
            'INSERT INTO transactions (user_id, item_id, borrow_date, return_date) VALUES (?, ?, ?, NULL)',
            (user_id, item_id, now)
        )
        # Mark item unavailable
        self.cursor.execute(
            'UPDATE items SET available=0 WHERE id=?', (item_id,)
        )
        self.conn.commit()
        print(f"{self.get_item_name(item_id)} borrowed on {now}")

    def return_item(self, user_id, item_id):
        # Find open transaction
        tx = self.cursor.execute(
            'SELECT id, borrow_date FROM transactions WHERE user_id=? AND item_id=? AND return_date IS NULL',
            (user_id, item_id)
        ).fetchone()
        if not tx:
            print("No outstanding borrow found for that item.")
            return
        now = datetime.now().strftime(DATE_FMT)
        # Update return date
        self.cursor.execute(
            'UPDATE transactions SET return_date=? WHERE id=?',
            (now, tx['id'])
        )
        # Mark item available
        self.cursor.execute(
            'UPDATE items SET available=1 WHERE id=?', (item_id,)
        )
        # Late penalty prompt
        late = input("Was this return late? (y/n): ").strip().lower()
        if late == 'y':
            print("Late return! -5 credits applied.")
            self.cursor.execute(
                'UPDATE users SET credits = MAX(credits - 5, 0) WHERE id=?', (user_id,)
            )
        else:
            print(f"{self.get_item_name(item_id)} returned on time.")
        self.conn.commit()

    def view_history(self, user_id):
        user = self.cursor.execute(
            'SELECT name, credits FROM users WHERE id=?', (user_id,)
        ).fetchone()
        print(f"\nTransaction history for {user['name']}:")
        rows = self.cursor.execute(
            '''
            SELECT t.borrow_date, t.return_date, i.name
            FROM transactions t
            JOIN items i ON t.item_id = i.id
            WHERE t.user_id=?
            ORDER BY t.borrow_date ASC
            ''', (user_id,)
        ).fetchall()
        for r in rows:
            status = 'Returned' if r['return_date'] else 'Still out'
            date = r['return_date'] or r['borrow_date']
            print(f"- {status} {r['name']} at {date}")
        print(f"Credits remaining: {user['credits']}\n")

    def get_item_name(self, item_id):
        row = self.cursor.execute(
            'SELECT name FROM items WHERE id=?', (item_id,)
        ).fetchone()
        return row['name'] if row else 'Unknown Item'

    def list_users(self):
        users = self.cursor.execute('SELECT id, name, credits FROM users').fetchall()
        print("Select a user:")
        for u in users:
            print(f"{u['id']}: {u['name']} (Credits: {u['credits']})")


def main():
    gm = GameManager()
    print("Welcome to the Halo Reach Armory (Phase 2 - DB Mode)!")

    # User selection
    while True:
        gm.list_users()
        try:
            uid = int(input("Choice: "))
            if gm.cursor.execute('SELECT 1 FROM users WHERE id=?', (uid,)).fetchone():
                break
        except ValueError:
            pass
        print("Invalid user selection.\n")

    # Main loop
    while True:
        print("\nMenu:")
        print("1. List available items")
        print("2. Borrow an item")
        print("3. Return an item")
        print("4. View history & credits")
        print("5. Quit")
        choice = input("Choice: ").strip()
        if choice == '1':
            gm.list_items()
        elif choice == '2':
            gm.list_items()
            try:
                iid = int(input("Enter item ID to borrow: "))
                gm.borrow_item(uid, iid)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '3':
            try:
                iid = int(input("Enter item ID to return: "))
                gm.return_item(uid, iid)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '4':
            gm.view_history(uid)
        elif choice == '5':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == '__main__':
    main()