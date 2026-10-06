"""Fetch books from Open Library, store them in SQLite, and display them."""

from __future__ import annotations

import logging
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any

import requests

API_URL = "https://openlibrary.org/search.json"
DATABASE_PATH = Path(__file__).with_name("books.db")
TIMEOUT_SECONDS = 15


def parse_books(payload: Any) -> list[tuple[str, str, int | None]]:
    """Map Open Library docs to title, author, publication year."""
    if not isinstance(payload, dict) or not isinstance(payload.get("docs"), list):
        raise ValueError("API response must be an object containing a docs list")
    books: list[tuple[str, str, int | None]] = []
    for index, item in enumerate(payload["docs"]):
        if not isinstance(item, dict):
            logging.warning("Skipping book %d: entry is not an object", index)
            continue
        title = item.get("title")
        authors = item.get("author_name")
        year = item.get("first_publish_year")
        if not isinstance(title, str) or not title.strip():
            logging.warning("Skipping book %d: missing title", index)
            continue
        author = authors[0] if isinstance(authors, list) and authors and isinstance(authors[0], str) else "Unknown"
        if year is not None and (not isinstance(year, int) or isinstance(year, bool)):
            logging.warning("Book %r has an invalid publication year; storing it as NULL", title)
            year = None
        books.append((title.strip(), author, year))
    return books


def fetch_books(query: str = "machine learning", limit: int = 10) -> list[tuple[str, str, int | None]]:
    try:
        response = requests.get(API_URL, params={"q": query, "limit": limit}, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError(f"The books API returned invalid JSON: {exc}") from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not retrieve books from {API_URL}: {exc}") from exc
    return parse_books(payload)


def save_books(books: list[tuple[str, str, int | None]], database_path: Path = DATABASE_PATH) -> None:
    try:
        with closing(sqlite3.connect(database_path)) as connection:
            with connection:
                connection.execute("""CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publication_year INTEGER
                )""")
                connection.execute("DELETE FROM books")
                connection.executemany(
                    "INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)", books
                )
    except sqlite3.Error as exc:
        raise RuntimeError(f"Could not save books to {database_path}: {exc}") from exc


def read_books(database_path: Path = DATABASE_PATH) -> list[tuple[str, str, int | None]]:
    try:
        with closing(sqlite3.connect(database_path)) as connection:
            return connection.execute(
                "SELECT title, author, publication_year FROM books ORDER BY title"
            ).fetchall()
    except sqlite3.Error as exc:
        raise RuntimeError(f"Could not read books from {database_path}: {exc}") from exc


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    books = fetch_books()
    if not books:
        raise RuntimeError("The API response contained no valid books")
    save_books(books)
    print(f"Stored and retrieved {len(books)} books:")
    for title, author, year in read_books():
        print(f"- {title} | {author} | {year if year is not None else 'Unknown year'}")


if __name__ == "__main__":
    main()
