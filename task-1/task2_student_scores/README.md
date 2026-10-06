# Task 2: Student math scores

This task retrieves individual student records over HTTPS, calculates the average math test score, and creates a bar chart. It uses the API response directly; `data/student_scores.json` is not read by this task.

## Data source

- **API URL:** `https://api.slingacademy.com/v1/sample-data/files/student-scores.json`
- **API source:** [Sling Academy Student Scores sample data](https://www.slingacademy.com/article/student-scores-sample-data-csv-json-xlsx-xml/)
- **Selected field:** `math_score`

The source documents individual student records, including first and last names and subject scores from 0 to 100. `math_score` is selected as the single test score for this assignment because it is a numeric subject score provided for each student and lets the per-student mean and bar chart use a consistent measure.

## Calculation and assumptions

The script parses the JSON list of individual records. A record is included only when it has nonblank string values for `first_name` and `last_name` and a finite numeric `math_score` from 0 through 100. Missing, malformed, nonnumeric, boolean, non-finite, or out-of-range score records are skipped. If no valid records remain, the task stops with a clear error. Names are displayed as `first_name last_name`; duplicate names remain separate records. The printed processed count is the number of valid records included in the calculation and chart.

The arithmetic mean is calculated as the sum of valid math scores divided by the number of valid math scores. Every valid student contributes equally; no weighting is applied. The source describes this as sample data, so the records should be treated as educational/sample data rather than verified real student results.

## Error handling and output

The fetch uses `requests` with a 20-second timeout. Timeout, other network errors, HTTP errors, invalid JSON, an unexpected JSON structure, and a response with no valid records are reported clearly. A chart is saved to `task2_student_scores/output/student_scores.png`.

From the `task-1` directory, run:

```bash
python task2_student_scores/main.py
```

The script prints the number of valid records processed and the arithmetic average math score. From the repository root, install dependencies with `python -m pip install -r requirements.txt` before running the task.

## Tests

The Task 2 parsing and average tests use in-memory records, and the API-fetch tests mock the HTTP response. They do not rely on a live network.


