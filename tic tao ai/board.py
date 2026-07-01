"""Tic-Tac-Toe board state and game rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

EMPTY = 0
X = 1
O = -1

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

SYMBOLS = {EMPTY: ".", X: "X", O: "O"}


@dataclass(frozen=True)
class Board:
    cells: tuple[int, ...] = (EMPTY,) * 9

    def with_move(self, index: int, player: int) -> Board:
        if self.cells[index] != EMPTY:
            raise ValueError(f"Cell {index} is already occupied")
        cells = list(self.cells)
        cells[index] = player
        return Board(tuple(cells))

    def legal_moves(self) -> Iterator[int]:
        for i, cell in enumerate(self.cells):
            if cell == EMPTY:
                yield i

    def winner(self) -> int | None:
        for a, b, c in WIN_LINES:
            line = self.cells[a], self.cells[b], self.cells[c]
            if line[0] != EMPTY and line[0] == line[1] == line[2]:
                return line[0]
        return None

    def is_terminal(self) -> bool:
        return self.winner() is not None or EMPTY not in self.cells

    def render(self) -> str:
        rows = []
        for row in range(3):
            cells = [SYMBOLS[self.cells[row * 3 + col]] for col in range(3)]
            rows.append(" | ".join(cells))
        return "\n---------\n".join(rows)

    def render_with_positions(self) -> str:
        labels = [str(i) if self.cells[i] == EMPTY else SYMBOLS[self.cells[i]] for i in range(9)]
        rows = []
        for row in range(3):
            rows.append(" | ".join(labels[row * 3 : row * 3 + 3]))
        return "\n---------\n".join(rows)
