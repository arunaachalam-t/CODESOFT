#!/usr/bin/env python3
"""Demo CLI for the movie recommendation system."""

import argparse

from recommender import CollaborativeRecommender, ContentBasedRecommender, HybridRecommender


def print_recommendations(title: str, recommendations: list[dict]) -> None:
  print(f"\n{title}")
  print("-" * len(title))
  if not recommendations:
    print("No recommendations found.")
    return

  for i, rec in enumerate(recommendations, start=1):
    movie = rec["movie"]
    genres = ", ".join(movie["genres"])
    print(
      f"{i}. {movie['title']} ({movie['year']}) - {genres} - "
      + ", ".join(f"{k}: {v}" for k, v in rec.items() if k != "movie")
    )


def main() -> None:
  parser = argparse.ArgumentParser(description="Simple movie recommendation system")
  parser.add_argument(
    "--method",
    choices=["content", "collaborative", "hybrid"],
    default="hybrid",
    help="Recommendation strategy to use",
  )
  parser.add_argument("--user", default="alice", help="User ID for collaborative/hybrid mode")
  parser.add_argument(
    "--liked",
    nargs="+",
    type=int,
    default=[1, 2, 3],
    help="Movie IDs the user likes (content-based mode)",
  )
  parser.add_argument("--top", type=int, default=5, help="Number of recommendations")
  parser.add_argument(
    "--similar-to",
    type=int,
    help="Show movies similar to this movie ID (content-based only)",
  )
  args = parser.parse_args()

  if args.similar_to is not None:
    content = ContentBasedRecommender()
    recs = content.similar_items(args.similar_to, top_n=args.top)
    print_recommendations(f"Movies similar to ID {args.similar_to}", recs)
    return

  if args.method == "content":
    content = ContentBasedRecommender()
    recs = content.recommend(args.liked, top_n=args.top)
    print_recommendations("Content-based recommendations", recs)
  elif args.method == "collaborative":
    collab = CollaborativeRecommender()
    recs = collab.recommend(args.user, top_n=args.top)
    print_recommendations(f"Collaborative recommendations for '{args.user}'", recs)
  else:
    hybrid = HybridRecommender()
    recs = hybrid.recommend(args.user, top_n=args.top)
    print_recommendations(f"Hybrid recommendations for '{args.user}'", recs)


if __name__ == "__main__":
  main()
