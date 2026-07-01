from .utils import cosine_similarity, load_json


class ContentBasedRecommender:
  """Recommends items similar to ones the user already likes, based on item features."""

  def __init__(self, movies: list[dict] | None = None):
    self.movies = movies or load_json("movies.json")
    self._movie_by_id = {m["id"]: m for m in self.movies}
    self._feature_vectors = self._build_feature_vectors()

  def _build_feature_vectors(self) -> dict[int, dict[str, float]]:
    vectors: dict[int, dict[str, float]] = {}
    for movie in self.movies:
      features: dict[str, float] = {}
      for genre in movie["genres"]:
        features[f"genre:{genre}"] = 1.0
      features[f"director:{movie['director']}"] = 1.0
      features["year_normalized"] = movie["year"] / 2100.0
      vectors[movie["id"]] = features
    return vectors

  def recommend(
    self,
    liked_movie_ids: list[int],
    top_n: int = 5,
    exclude_ids: list[int] | None = None,
  ) -> list[dict]:
    if not liked_movie_ids:
      return []

    exclude = set(exclude_ids or []) | set(liked_movie_ids)
    profile: dict[str, float] = {}

    for movie_id in liked_movie_ids:
      for feature, value in self._feature_vectors[movie_id].items():
        profile[feature] = profile.get(feature, 0.0) + value

    scored: list[tuple[float, dict]] = []
    for movie in self.movies:
      if movie["id"] in exclude:
        continue
      score = cosine_similarity(profile, self._feature_vectors[movie["id"]])
      if score > 0:
        scored.append((score, movie))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
      {"movie": movie, "score": round(score, 3), "reason": "similar content profile"}
      for score, movie in scored[:top_n]
    ]

  def similar_items(self, movie_id: int, top_n: int = 5) -> list[dict]:
    if movie_id not in self._movie_by_id:
      return []

    source = self._feature_vectors[movie_id]
    scored: list[tuple[float, dict]] = []

    for movie in self.movies:
      if movie["id"] == movie_id:
        continue
      score = cosine_similarity(source, self._feature_vectors[movie["id"]])
      scored.append((score, movie))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
      {"movie": movie, "score": round(score, 3)}
      for score, movie in scored[:top_n]
    ]
