from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.schemas import (
  Movie,
  RecommendationItem,
  RecommendationRequest,
  UserRating,
  UserSummary,
)
from recommender import CollaborativeRecommender, ContentBasedRecommender, HybridRecommender
from recommender.utils import load_json

ROOT = Path(__file__).parent.parent
STATIC_DIR = ROOT / "static"

content_recommender = ContentBasedRecommender()
collab_recommender = CollaborativeRecommender()
hybrid_recommender = HybridRecommender()

app = FastAPI(
  title="Movie Recommendation API",
  description="Content-based, collaborative, and hybrid movie recommendations",
  version="1.0.0",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def _normalize_recommendations(recs: list[dict], method: str) -> list[RecommendationItem]:
  items: list[RecommendationItem] = []
  for rec in recs:
    movie = Movie(**rec["movie"])
    details = {k: v for k, v in rec.items() if k not in ("movie", "reason")}

    if method == "content":
      score = float(rec.get("score", 0))
      score_label = "Similarity"
    elif method == "collaborative":
      score = float(rec.get("predicted_rating", 0))
      score_label = "Predicted rating"
    else:
      score = float(rec.get("hybrid_score", 0))
      score_label = "Hybrid score"

    items.append(
      RecommendationItem(
        movie=movie,
        score=round(score, 3),
        score_label=score_label,
        reason=rec.get("reason", ""),
        details=details,
      )
    )
  return items


@app.get("/")
async def serve_ui() -> FileResponse:
  return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health() -> dict[str, str]:
  return {"status": "ok"}


@app.get("/api/movies", response_model=list[Movie])
async def list_movies() -> list[Movie]:
  return [Movie(**m) for m in load_json("movies.json")]


@app.get("/api/movies/{movie_id}", response_model=Movie)
async def get_movie(movie_id: int) -> Movie:
  movies = {m["id"]: m for m in load_json("movies.json")}
  if movie_id not in movies:
    raise HTTPException(status_code=404, detail="Movie not found")
  return Movie(**movies[movie_id])


@app.get("/api/movies/{movie_id}/similar", response_model=list[RecommendationItem])
async def similar_movies(
  movie_id: int,
  top_n: int = Query(default=5, ge=1, le=20),
) -> list[RecommendationItem]:
  recs = content_recommender.similar_items(movie_id, top_n=top_n)
  if not recs:
    raise HTTPException(status_code=404, detail="Movie not found or no similar items")
  return _normalize_recommendations(
    [{**r, "reason": "similar content profile"} for r in recs],
    "content",
  )


@app.get("/api/users", response_model=list[UserSummary])
async def list_users() -> list[UserSummary]:
  return [
    UserSummary(user_id=user_id, rating_count=len(ratings))
    for user_id, ratings in collab_recommender._user_ratings.items()
  ]


@app.get("/api/users/{user_id}/ratings", response_model=list[UserRating])
async def user_ratings(user_id: str) -> list[UserRating]:
  ratings = collab_recommender._user_ratings.get(user_id)
  if ratings is None:
    raise HTTPException(status_code=404, detail="User not found")

  results: list[UserRating] = []
  for movie_id, rating in ratings.items():
    movie = collab_recommender._movie_by_id[movie_id]
    results.append(UserRating(movie_id=movie_id, title=movie["title"], rating=rating))

  results.sort(key=lambda r: r.rating, reverse=True)
  return results


@app.post("/api/recommendations", response_model=list[RecommendationItem])
async def recommend(request: RecommendationRequest) -> list[RecommendationItem]:
  method = request.method
  top_n = request.top_n

  if method in ("collaborative", "hybrid"):
    if not request.user_id:
      raise HTTPException(status_code=400, detail="user_id is required for this method")
    if request.user_id not in collab_recommender._user_ratings:
      raise HTTPException(status_code=404, detail="User not found")

  if method == "content":
    if not request.liked_movie_ids:
      raise HTTPException(status_code=400, detail="liked_movie_ids is required for content-based mode")
    recs = content_recommender.recommend(request.liked_movie_ids, top_n=top_n)
  elif method == "collaborative":
    recs = collab_recommender.recommend(request.user_id, top_n=top_n)
  else:
    recs = hybrid_recommender.recommend(request.user_id, top_n=top_n)

  return _normalize_recommendations(recs, method)
