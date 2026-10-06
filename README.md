# AccuKnox AI/ML Trainee Technical Submission

This repository contains the existing work for both AccuKnox problem statements. The implementation and written responses are organized below without adding technical answers beyond the material provided.

## Problem Statement 1

The `task-1/` directory contains the three existing exercises:

- **Books API:** fetches Open Library book records, stores them in SQLite, and displays the retrieved rows.
- **Student scores:** fetches Sling Academy sample/fictional score records, parses `math_score`, calculates the arithmetic mean, and plots student names and scores. No local student-score JSON file is required.
- **CSV import:** validates `name` and `email` rows from `data/users.csv`, inserts them into SQLite, and displays the saved rows.

The requested personal-code references are included below. They point to the existing `groqchat-api` repository; its source is not copied here.

## Problem Statement 2

The existing written response is in [`task-2/README.md`](task-2/README.md). It contains the self-ratings, high-level LLM chatbot architecture, and Qdrant selection discussion.

## Install and run

Use Python 3.10 or newer. From the repository root:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python task-1/task1_books_api/main.py
python task-1/task2_student_scores/main.py
python task-1/task3_csv_import/main.py
```

Tasks 1 and 2 require network access. Tasks 1 and 3 create SQLite databases at runtime. Task 2 saves its chart under its task directory at runtime. These generated files are ignored by Git.

## Tests

Run the existing six offline unit tests from the `task-1/` directory:

```bash
cd task-1
python -m unittest discover -s tests -v
```

## Personal code references

**Most complex Python code personally written:** [app/services/llm_service.py](https://github.com/MahaMugeshAnanth/groqchat-api/blob/main/app/services/llm_service.py)

**Most complex database code personally written:** [app/db/repository.py](https://github.com/MahaMugeshAnanth/groqchat-api/blob/main/app/db/repository.py)

Related database models: [app/models/db_models.py](https://github.com/MahaMugeshAnanth/groqchat-api/blob/main/app/models/db_models.py)
