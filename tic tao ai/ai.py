"""Unbeatable Tic-Tac-Toe AI using Minimax with Alpha-Beta pruning."""

from __future__ import annotations

from board import Board, EMPTY


def minimax(
    board: Board,
    ai_player: int,
    is_maximizing: bool,
    alpha: int = float("-inf"),
    beta: int = float("inf"),
    depth: int = 0,
) -> int:
    winner = board.winner()
    if winner is not None:
        return (10 - depth) if winner == ai_player else (depth - 10)
    if EMPTY not in board.cells:
        return 0

    if is_maximizing:
        best = float("-inf")
        for move in board.legal_moves():
            score = minimax(
                board.with_move(move, ai_player),
                ai_player,
                False,
                alpha,
                beta,
                depth + 1,
            )
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return int(best)

    best = float("inf")
    for move in board.legal_moves():
        score = minimax(
            board.with_move(move, -ai_player),
            ai_player,
            True,
            alpha,
            beta,
            depth + 1,
        )
        best = min(best, score)
        beta = min(beta, best)
        if beta <= alpha:
            break
    return int(best)


def best_move(board: Board, ai_player: int) -> int:
    best_score = float("-inf")
    chosen = -1

    for move in board.legal_moves():
        score = minimax(board.with_move(move, ai_player), ai_player, False)
        if score > best_score:
            best_score = score
            chosen = move

    if chosen == -1:
        raise RuntimeError("No legal moves available")
    return chosen
