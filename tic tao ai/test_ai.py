"""Verify the AI never loses against random opponents."""

from __future__ import annotations

import random

from ai import best_move
from board import Board, EMPTY, O, X


def play_random_vs_ai(ai_player: int, ai_first: bool) -> int | None:
    board = Board()
    current = ai_player if ai_first else -ai_player

    while not board.is_terminal():
        if current == ai_player:
            move = best_move(board, ai_player)
        else:
            move = random.choice(list(board.legal_moves()))
        board = board.with_move(move, current)
        current = -current

    return board.winner()


def main() -> None:
    trials = 500
    ai_losses = 0

    for _ in range(trials):
        ai = random.choice([X, O])
        ai_first = random.choice([True, False])
        winner = play_random_vs_ai(ai, ai_first)
        if winner == -ai:
            ai_losses += 1

    print(f"Trials: {trials}")
    print(f"AI losses: {ai_losses}")
    assert ai_losses == 0, "AI should never lose to random play"
    print("AI is unbeatable against random opponents.")


if __name__ == "__main__":
    main()
