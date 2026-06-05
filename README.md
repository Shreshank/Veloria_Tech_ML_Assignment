# Incomplete Test Readme, Will further improve as completing assignment

# Veloria Tech — ML Intern Assignment
**Submitted by:** Shreshank Kesharwani
**Date:** 05 June 2026
**Email:** shivankkesharwani4@gmail.com

---

## Overview

This repository contains my submission for the Veloria Tech AI/ML Engineering Internship assignment. It includes a cricket data web scraper, a match outcome prediction model, and a semantic search system built with vector embeddings.

---

## Repository Structure

```
veloria-tech-ml-intern-assignment/
│
├── trails              # Experiments done before writing final code
├── requirements.txt    # To Downnload all necessary libraries
├── scraper.py          # Task 1 — Web scraping script
├── match_data.csv      # Task 1 — Scraped match data output
├── model.py            # Task 2 — ML prediction model
├── rag_search.py       # Task 3 (Bonus) — Semantic search with vector embeddings
└── README.md           # This file
```

---

## Setup — Install Dependencies

Make sure you have Python 3.8+ installed, then run:

```bash
pip install -r requirements.txt
```

---

## Task 1 — Web Scraping (`scraper.py`)

### What it does
Scrapes the ipl 2026 cricket matches from [ESPNCricinfo].

For each match, it collects:
- `Match_no` | Match identifier (e.g., "1st Match", "Final") |
- `Date` | Date of the match (YYYY-MM-DD) |
- `Team1` | Home / first team |
- `Team2` | Away / second team |
- `Venue` | Stadium and city |
- `Winning_team` | Winner of the match (includes Super Over results) |
- `Player_of_match` | Player awarded Man of the Match |
- `Player_of_match_total_impact` | Impact score of the Player of the Match |
- `Top_scorer` | Highest run-scorer in the match |
- `Top_scorer_runs` | Runs scored by the top scorer |

Results are saved to `match_data.csv`.

### How to run

- Create a datas and trials/data(for Experiments.ipynb) folder

```bash
python scraper.py
```

**Output:** `match_data.csv` in the same directory.

---

## Task 2 — ML Prediction Model (`model.py`)

### What it does
Loads `trials/matches.csv`, engineers features, trains a classification model to predict match outcomes, and evaluates performance.

### Algorithm used
**[Logistic Regression]**

*Reason:* Logistic Regression was chosen as a clean baseline given the small dataset size. It is interpretable and performs well on binary classification tasks.

### Features used
- venue
- main_team
- opposing_team
- toss_decision
- main_team_won_toss

### How to run

```bash
python model.py
```

### Results

| Metric | Score |
|--------|-------|
| Accuracy | 57(training) | 52(test)
| F1 Score | 57(training) | 52(test)

**Confusion Matrix:**

```
[[274 261]
 [202 353]]

[[55 55]
 [44 64]]
```

> ![Output](image.png)

---

## Task 3 (Bonus) — Semantic Search (`rag_search.py`)

### What it does
Converts each match record into a descriptive text sentence, generates vector embeddings using `sentence-transformers`, stores them in ChromaDB, and allows semantic queries to retrieve the most relevant matches.

### How to run

```bash
python rag_search.py
```

You will be prompted to enter a search query. Example:

```
Enter your search query: Show me matches where the away team won
```

**Output:** Top 3 most semantically similar match records.

### How it works
1. Each row in `trials/matches.csv` is converted into a natural language sentence — e.g. *"India vs Australia at MCG on 15 Jan 2024. Australia won. Top scorer: David Warner with 87 runs."*
2. `sentence-transformers` (model: `model_name`) encodes each sentence into a dense vector.
3. Vectors are stored in a ChromaDB in-memory collection.
4. On query, the query string is also embedded and cosine similarity is used to retrieve the top 3 matches.

---

## Challenges Faced

- [Website structure changed — had to adjust CSS selectors]
- [Small dataset and features size limited model accuracy]

---

## Demo Video

🎥 **Loom walkthrough:** [Loom link]

---

## Contact

[Shreshank Kesharwani] — [shivankkesharwani4@gmail.com] — [9165016666]
