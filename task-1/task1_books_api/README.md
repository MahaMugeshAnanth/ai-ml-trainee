# Task 1: Books API and SQLite

Fetches up to ten results for `machine learning` from Open Library Search API (`https://openlibrary.org/search.json?q=machine%20learning&limit=10`), maps the response, stores it in `books.db`, then selects and displays the stored rows. The response is an object with a `docs` array. Each document may include `title`, `author_name` (an array), and `first_publish_year`.

Mapping: `title` → `title`; first `author_name` value → `author` (or `Unknown` if absent); `first_publish_year` → `publication_year` (or SQL `NULL` if absent/invalid). Invalid entries without a title are skipped. Each run replaces the previous retrieved rows so the database reflects the latest fetch. HTTP/network errors, timeouts, invalid JSON/shape, and SQLite errors produce clear failures.

Run from the `assignment_1` directory with `python task1_books_api/main.py`. Requires the packages in `requirements.txt` and network access.
