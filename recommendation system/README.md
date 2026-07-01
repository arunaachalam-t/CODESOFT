# Movie Recommendation System

A Python recommendation system that suggests movies using three strategies:

- **Content-based filtering** — recommends movies similar to ones you like (genre, director, year)
- **Collaborative filtering** — recommends movies liked by users with similar taste
- **Hybrid** — combines both approaches

Includes a **CLI**, **REST API**, and **web UI**.

## Project structure

```
data/
  movies.json          # Movie catalog with features
  ratings.json         # User ratings
recommender/
  content_based.py
  collaborative.py
  hybrid.py
  utils.py
api/
  app.py               # FastAPI REST API
  schemas.py
static/
  index.html           # Web UI
  css/style.css
  js/app.js
main.py                # CLI demo
requirements.txt
```

## Requirements

- Python 3.10+

## Setup

```bash
pip install -r requirements.txt
```

## Web UI & API

Start the server:

```bash
py -m uvicorn api.app:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

Interactive API docs: **http://127.0.0.1:8000/docs**

### API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/movies` | List all movies |
| GET | `/api/movies/{id}` | Get a movie |
| GET | `/api/movies/{id}/similar` | Content-based similar movies |
| GET | `/api/users` | List users |
| GET | `/api/users/{id}/ratings` | User rating history |
| POST | `/api/recommendations` | Get recommendations |

**Example — hybrid recommendations for Alice:**

```bash
curl -X POST http://127.0.0.1:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d "{\"method\": \"hybrid\", \"user_id\": \"alice\", \"top_n\": 5}"
```

**Example — content-based recommendations:**

```bash
curl -X POST http://127.0.0.1:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d "{\"method\": \"content\", \"liked_movie_ids\": [1, 2, 3], \"top_n\": 5}"
```

## CLI usage

**Hybrid recommendations for a user (default):**

```bash
py main.py --user alice
```

**Collaborative filtering:**

```bash
py main.py --method collaborative --user dave
```

**Content-based filtering (based on liked movie IDs):**

```bash
py main.py --method content --liked 1 2 3
```

**Find movies similar to a specific title:**

```bash
py main.py --similar-to 2
```

## How it works

### Content-based filtering

Each movie is represented as a feature vector (genres, director, normalized year). The system builds a profile from movies the user likes and scores unrated movies using cosine similarity.

### Collaborative filtering

User ratings form a sparse matrix. For a target user, the system finds similar users via cosine similarity on their rating vectors, then predicts ratings for unseen movies using a weighted average of similar users' ratings.

### Hybrid

Normalizes collaborative predicted ratings and content similarity scores, then blends them (60% collaborative, 40% content by default).

## Sample users

| User  | Taste profile                          |
|-------|----------------------------------------|
| alice | Sci-fi / Nolan films                   |
| bob   | Action / Tarantino                     |
| carol | Animation / family                     |
| dave  | Sci-fi (Villeneuve, Nolan)             |
| eve   | Drama                                  |

## Extending

- Add books or products by creating new JSON catalogs with relevant features
- Swap in matrix factorization (e.g. SVD) for larger datasets
- Add user authentication and persistent ratings storage
