"""Validate users from CSV, store them in SQLite, and display the rows."""

from __future__ import annotations

import csv
import re
import sqlite3
from contextlib import closing
from pathlib import Path

CSV_PATH = Path(__file__).parents[1] / "data" / "users.csv"
DATABASE_PATH = Path(__file__).with_name("users.db")
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def read_users(path: Path = CSV_PATH) -> list[tuple[str, str]]:
    users: list[tuple[str, str]] = []
    seen_emails: set[str] = set()
    try:
        with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            if not reader.fieldnames or not {"name", "email"}.issubset(reader.fieldnames):
                raise ValueError("CSV must contain name and email columns")
            for line_number, row in enumerate(reader, start=2):
                if None in row:
                    raise ValueError(f"CSV line {line_number} has more values than the header")
                name = (row.get("name") or "").strip()
                email = (row.get("email") or "").strip()
                if not name or not EMAIL_PATTERN.fullmatch(email):
                    raise ValueError(f"CSV line {line_number} has a missing name or invalid email")
                email_key = email.casefold()
                if email_key in seen_emails:
                    continue
                seen_emails.add(email_key)
                users.append((name, email))
    except OSError as exc:
        raise RuntimeError(f"Could not read CSV {path}: {exc}") from exc
    return users


def save_users(users: list[tuple[str, str]], path: Path = DATABASE_PATH) -> None:
    try:
        with closing(sqlite3.connect(path)) as connection:
            with connection:
                connection.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE COLLATE NOCASE
                )""")
                connection.execute("DELETE FROM users")
                connection.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)
    except sqlite3.Error as exc:
        raise RuntimeError(f"Could not import users into {path}: {exc}") from exc


def read_saved_users(path: Path = DATABASE_PATH) -> list[tuple[str, str]]:
    try:
        with closing(sqlite3.connect(path)) as connection:
            return connection.execute("SELECT name, email FROM users ORDER BY name").fetchall()
    except sqlite3.Error as exc:
        raise RuntimeError(f"Could not read users from {path}: {exc}") from exc


def main() -> None:
    users = read_users()
    save_users(users)
    print(f"Imported {len(users)} users:")
    for name, email in read_saved_users():
        print(f"- {name} | {email}")


if __name__ == "__main__":
    main()
