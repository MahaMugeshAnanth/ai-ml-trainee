# Task 3: CSV to SQLite

Reads `data/users.csv` with Python's `csv` module, requires non-empty `name` and a basic valid email format, skips duplicate email addresses case-insensitively, then replaces the database rows and displays the saved users. Malformed required fields fail with the CSV line number; database errors are reported.

Schema: `users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE COLLATE NOCASE)`. Run from the `task-1` directory with `python task3_csv_import/main.py`.

