from typing import Literal

from pydantic import BaseModel, Field


class Movie(BaseModel):
  id: int
  title: str
  genres: list[str]
  director: str
  year: int


class UserRating(BaseModel):
  movie_id: int
  title: str
  rating: float


class UserSummary(BaseModel):
  user_id: str
  rating_count: int


class RecommendationRequest(BaseModel):
  method: Literal["content", "collaborative", "hybrid"] = "hybrid"
  user_id: str | None = None
  liked_movie_ids: list[int] = Field(default_factory=list)
  top_n: int = Field(default=5, ge=1, le=20)


class RecommendationItem(BaseModel):
  movie: Movie
  score: float
  score_label: str
  reason: str
  details: dict[str, float | str] = Field(default_factory=dict)
