"""Play Tic-Tac-Toe against an unbeatable AI."""

from __future__ import annotations

import sys

from ai import best_move
from board import Board, EMPTY, O, X, SYMBOLS


def prompt_choice(prompt: str, options: dict[str, object]) -> object:
    keys = "/".join(options)
    while True:
        raw = input(f"{prompt} ({keys}): ").strip().lower()
        if raw in options:
            return options[raw]
        print(f"Please enter one of: {keys}")


def prompt_move(board: Board) -> int:
    while True:
        raw = input("Your move (0-8, or 'q' to quit): ").strip().lower()
        if raw == "q":
            print("Thanks for playing!")
            sys.exit(0)
        if not raw.isdigit():
            print("Enter a number from 0 to 8.")
            continue
        index = int(raw)
        if index not in range(9):
            print("Position must be between 0 and 8.")
            continue
        if board.cells[index] != EMPTY:
            print("That cell is already taken.")
            continue
        return index


def announce_result(board: Board, human: int) -> None:
    winner = board.winner()
    if winner == human:
        print("You win! (This should not happen against a perfect AI.)")
    elif winner == -human:
        print("AI wins.")
    else:
        print("It's a draw.")


def play_round(human: int, human_starts: bool) -> None:
    board = Board()
    ai = -human
    current = human if human_starts else ai

    print("\nPositions:")
    print(
        " 0 | 1 | 2 \n"
        "---------\n"
        " 3 | 4 | 5 \n"
        "---------\n"
        " 6 | 7 | 8 "
    )
    print()

    while not board.is_terminal():
        print(board.render_with_positions())
        print()

        if current == human:
            move = prompt_move(board)
            board = board.with_move(move, human)
        else:
            move = best_move(board, ai)
            print(f"AI plays {SYMBOLS[ai]} at position {move}")
            board = board.with_move(move, ai)

        current = -current

    print(board.render_with_positions())
    print()
    announce_result(board, human)


def main() -> None:
    print("=" * 40)
    print("  TIC-TAC-TOE  —  Human vs Unbeatable AI")
    print("=" * 40)
    print("The AI uses Minimax with Alpha-Beta pruning.\n")

    human = prompt_choice("Choose your symbol", {"x": X, "o": O})
    human_starts = prompt_choice("Do you want to go first?", {"y": True, "n": False})

    while True:
        play_round(human, human_starts)
        again = prompt_choice("Play again?", {"y": True, "n": False})
        if not again:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
