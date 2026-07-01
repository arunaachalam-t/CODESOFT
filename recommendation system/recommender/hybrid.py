from .collaborative import CollaborativeRecommender
from .content_based import ContentBasedRecommender


class HybridRecommender:
  """Combines collaborative and content-based scores for richer recommendations."""

  def __init__(
    self,
    collaborative_weight: float = 0.6,
    content_weight: float = 0.4,
  ):
    self.collaborative = CollaborativeRecommender()
    self.content = ContentBasedRecommender()
    self.collaborative_weight = collaborative_weight
    self.content_weight = content_weight

  def recommend(self, user_id: str, top_n: int = 5) -> list[dict]:
    collab = self.collaborative.recommend(user_id, top_n=20)
    liked_ids = list(self.collaborative._user_ratings.get(user_id, {}).keys())
    content = self.content.recommend(liked_ids, top_n=20, exclude_ids=liked_ids)

    scores: dict[int, dict] = {}

    for item in collab:
      movie_id = item["movie"]["id"]
      scores[movie_id] = {
        "movie": item["movie"],
        "collab_score": item["predicted_rating"] / 5.0,
        "content_score": 0.0,
      }

    for item in content:
      movie_id = item["movie"]["id"]
      if movie_id not in scores:
        scores[movie_id] = {
          "movie": item["movie"],
          "collab_score": 0.0,
          "content_score": item["score"],
        }
      else:
        scores[movie_id]["content_score"] = item["score"]

    ranked = []
    for movie_id, data in scores.items():
      hybrid_score = (
        self.collaborative_weight * data["collab_score"]
        + self.content_weight * data["content_score"]
      )
      ranked.append((hybrid_score, data["movie"], data))

    ranked.sort(key=lambda x: x[0], reverse=True)
    return [
      {
        "movie": movie,
        "hybrid_score": round(score, 3),
        "collaborative_component": round(data["collab_score"], 3),
        "content_component": round(data["content_score"], 3),
        "reason": "blend of user similarity and item similarity",
      }
      for score, movie, data in ranked[:top_n]
    ]
