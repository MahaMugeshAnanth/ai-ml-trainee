"""Offline validation of parsing and SQLite operations."""

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from task1_books_api import main as books
from task2_student_scores import main as scores
from task3_csv_import import main as users


class AssignmentTests(unittest.TestCase):
    def test_books_parse_and_database_round_trip(self):
        parsed = books.parse_books({"docs": [
            {"title": "A Book", "author_name": ["A. Author"], "first_publish_year": 2020},
            {"title": "No author"},
            {"author_name": ["Missing title"]},
        ]})
        self.assertEqual(parsed, [("A Book", "A. Author", 2020), ("No author", "Unknown", None)])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "books.db"
            books.save_books(parsed, path)
            self.assertEqual(books.read_books(path), [("A Book", "A. Author", 2020), ("No author", "Unknown", None)])
            with closing(sqlite3.connect(path)) as connection:
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM books").fetchone()[0], 2)

    @patch("task1_books_api.main.requests.get")
    def test_books_api_failure_is_clear(self, get):
        get.side_effect = books.requests.Timeout("timed out")
        with self.assertRaisesRegex(RuntimeError, "Could not retrieve books"):
            books.fetch_books()

    def test_math_score_parsing_average_and_invalid_records(self):
        parsed = scores.parse_scores([
            {"id": 1, "first_name": "Ada", "last_name": "Lovelace", "math_score": 80},
            {"id": 2, "first_name": "Grace", "last_name": "Hopper", "math_score": 90},
            {"id": 3, "first_name": "No", "last_name": "Score", "math_score": None},
            {"id": 4, "first_name": "Out", "last_name": "OfRange", "math_score": 101},
        ])
        self.assertEqual(parsed, [("Ada Lovelace", 80.0), ("Grace Hopper", 90.0)])
        self.assertEqual(scores.calculate_average(parsed), 85)
        with self.assertRaisesRegex(ValueError, "no valid"):
            scores.parse_scores([{"first_name": "Ada", "last_name": "Lovelace", "math_score": None}])
        with self.assertRaises(ValueError):
            scores.parse_scores({"records": []})

    @patch("task2_student_scores.main.requests.get")
    def test_score_fetch_uses_api_and_handles_http_failure(self, get):
        response = get.return_value
        response.json.return_value = [{
            "first_name": "Ada", "last_name": "Lovelace", "math_score": 80,
        }]
        self.assertEqual(scores.fetch_scores(), [("Ada Lovelace", 80.0)])
        get.assert_called_once_with(scores.API_URL, timeout=scores.REQUEST_TIMEOUT_SECONDS)
        get.reset_mock()
        get.side_effect = scores.requests.Timeout("timed out")
        with self.assertRaisesRegex(RuntimeError, "Timed out"):
            scores.fetch_scores()

    @patch("task2_student_scores.main.requests.get")
    def test_score_fetch_handles_invalid_json_and_http_status(self, get):
        get.return_value.json.side_effect = ValueError("bad JSON")
        with self.assertRaisesRegex(RuntimeError, "invalid JSON"):
            scores.fetch_scores()
        get.return_value.json.side_effect = None
        get.return_value.json.return_value = []
        get.return_value.raise_for_status.side_effect = scores.requests.HTTPError("404")
        with self.assertRaisesRegex(RuntimeError, "HTTP error"):
            scores.fetch_scores()

    def test_csv_validation_and_database_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "users.csv"
            csv_path.write_text("name,email\nAda,ada@example.com\nGrace,grace@example.com\nADA,ADA@example.com\n", encoding="utf-8")
            records = users.read_users(csv_path)
            self.assertEqual(records, [("Ada", "ada@example.com"), ("Grace", "grace@example.com")])
            db_path = Path(directory) / "users.db"
            users.save_users(records, db_path)
            self.assertEqual(users.read_saved_users(db_path), [("Ada", "ada@example.com"), ("Grace", "grace@example.com")])
            bad_csv = Path(directory) / "bad.csv"
            bad_csv.write_text("name,email\nNo email,\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "line 2"):
                users.read_users(bad_csv)
            extra_value_csv = Path(directory) / "extra.csv"
            extra_value_csv.write_text("name,email\nAda,ada@example.com,unexpected\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "more values than the header"):
                users.read_users(extra_value_csv)


if __name__ == "__main__":
    unittest.main()
