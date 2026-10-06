"""Fetch individual student math scores, calculate their mean, and chart them."""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any

import requests

# Keep Matplotlib's font cache inside the task folder, where it is writable.
MATPLOTLIB_CACHE = Path(__file__).with_name(".matplotlib")
MATPLOTLIB_CACHE.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MATPLOTLIB_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

API_URL = "https://api.slingacademy.com/v1/sample-data/files/student-scores.json"
CHART_PATH = Path(__file__).with_name("output") / "student_scores.png"
REQUEST_TIMEOUT_SECONDS = 20


def parse_scores(payload: Any) -> list[tuple[str, float]]:
    """Return valid (student name, math score) rows from API JSON records."""
    if not isinstance(payload, list):
        raise ValueError("API response must be a JSON list of student records")

    scores: list[tuple[str, float]] = []
    for row in payload:
        if not isinstance(row, dict):
            continue
        first_name, last_name = row.get("first_name"), row.get("last_name")
        score = row.get("math_score")
        if not all(isinstance(name, str) and name.strip() for name in (first_name, last_name)):
            continue
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            continue
        if not math.isfinite(score) or not 0 <= score <= 100:
            continue
        scores.append((f"{first_name.strip()} {last_name.strip()}", float(score)))

    if not scores:
        raise ValueError("API response contains no valid student math scores")
    return scores


def fetch_scores() -> list[tuple[str, float]]:
    """Fetch API records and return the valid names and math scores."""
    try:
        response = requests.get(API_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.Timeout as exc:
        raise RuntimeError(f"Timed out retrieving student scores: {exc}") from exc
    except requests.HTTPError as exc:
        raise RuntimeError(f"Student scores API returned an HTTP error: {exc}") from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not retrieve student scores: {exc}") from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("Student scores API returned invalid JSON") from exc
    try:
        return parse_scores(payload)
    except ValueError as exc:
        raise RuntimeError(f"Invalid student score data: {exc}") from exc


def calculate_average(scores: list[tuple[str, float]]) -> float:
    """Calculate the arithmetic mean of the valid math scores."""
    if not scores:
        raise ValueError("Cannot calculate an average without valid scores")
    return sum(score for _, score in scores) / len(scores)


def save_chart(scores: list[tuple[str, float]], path: Path = CHART_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names, values = zip(*scores)
    plt.figure(figsize=(12, 6))
    plt.bar(names, values, color="#3973ac")
    plt.title("Student Math Test Scores")
    plt.xlabel("Student")
    plt.ylabel("Math score (0–100)")
    plt.ylim(0, 100)
    plt.xticks(rotation=75, ha="right", fontsize=7)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def main() -> None:
    scores = fetch_scores()
    average = calculate_average(scores)
    save_chart(scores)
    print(f"Records processed: {len(scores)}")
    print(f"Average math score: {average:.2f}")
    print(f"Saved chart to: {CHART_PATH}")


if __name__ == "__main__":
    main()
