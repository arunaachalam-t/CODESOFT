from collections import defaultdict

from .utils import cosine_similarity, load_json


class CollaborativeRecommender:
  """Recommends items based on ratings from users with similar taste."""

  def __init__(self, ratings: list[dict] | None = None, movies: list[dict] | None = None):
    self.ratings = ratings or load_json("ratings.json")
    self.movies = movies or load_json("movies.json")
    self._movie_by_id = {m["id"]: m for m in self.movies}
    self._user_ratings = self._build_user_ratings()
    self._item_ratings = self._build_item_ratings()

  def _build_user_ratings(self) -> dict[str, dict[int, float]]:
    user_ratings: dict[str, dict[int, float]] = defaultdict(dict)
    for entry in self.ratings:
      user_ratings[entry["user_id"]][entry["movie_id"]] = entry["rating"]
    return dict(user_ratings)

  def _build_item_ratings(self) -> dict[int, dict[str, float]]:
    item_ratings: dict[int, dict[str, float]] = defaultdict(dict)
    for entry in self.ratings:
      item_ratings[entry["movie_id"]][entry["user_id"]] = entry["rating"]
    return dict(item_ratings)

  def _user_similarity(self, user_a: str, user_b: str) -> float:
    return cosine_similarity(self._user_ratings[user_a], self._user_ratings[user_b])

  def recommend(self, user_id: str, top_n: int = 5) -> list[dict]:
    if user_id not in self._user_ratings:
      return []

    target_ratings = self._user_ratings[user_id]
    seen = set(target_ratings)
    predictions: dict[int, tuple[float, float]] = {}

    for other_user, other_ratings in self._user_ratings.items():
      if other_user == user_id:
        continue

      similarity = self._user_similarity(user_id, other_user)
      if similarity <= 0:
        continue

      for movie_id, rating in other_ratings.items():
        if movie_id in seen:
          continue
        weighted_sum, weight_total = predictions.get(movie_id, (0.0, 0.0))
        predictions[movie_id] = (
          weighted_sum + similarity * rating,
          weight_total + abs(similarity),
        )

    scored: list[tuple[float, dict, float]] = []
    for movie_id, (weighted_sum, weight_total) in predictions.items():
      if weight_total == 0:
        continue
      predicted_rating = weighted_sum / weight_total
      scored.append((predicted_rating, self._movie_by_id[movie_id], weight_total))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
      {
        "movie": movie,
        "predicted_rating": round(score, 2),
        "confidence": round(weight, 2),
        "reason": "users with similar taste liked this",
      }
      for score, movie, weight in scored[:top_n]
    ]

  def top_rated_for_item(self, movie_id: int, top_n: int = 3) -> list[dict]:
    ratings = self._item_ratings.get(movie_id, {})
    ranked = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    return [{"user_id": user, "rating": rating} for user, rating in ranked[:top_n]]
