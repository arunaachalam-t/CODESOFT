# AI Tic-Tac-Toe

## Overview

This project implements an AI-powered Tic-Tac-Toe game where a human player competes against an intelligent computer opponent. The AI uses the **Minimax algorithm** to determine the optimal move, ensuring it never loses. This project demonstrates the application of game theory, adversarial search, and decision-making algorithms in Artificial Intelligence.

---

## Features

* Human vs AI gameplay.
* AI powered by the Minimax algorithm.
* Detects wins, losses, and draw conditions.
* Interactive command-line interface.
* Modular project structure for better code organization.
* Unit tests for validating AI functionality.

---

## Technologies Used

* Python 3.x
* Standard Python libraries
* `unittest` (for testing)

---

## Project Structure

```text
AI-Tic-Tac-Toe/
│
├── ai.py           # AI logic using the Minimax algorithm
├── board.py        # Game board and game rules
├── main.py         # Main program to start the game
├── test_ai.py      # Unit tests for AI behavior
├── README.md       # Project documentation
```

---

## Installation

1. Clone or download the repository.
2. Ensure Python 3.x is installed.
3. Open a terminal in the project directory.

---

## How to Run

Start the game with:

```bash
python main.py
```

If your system uses `python3`, run:

```bash
python3 main.py
```

---

## Running Tests

To verify the AI implementation, run:

```bash
python test_ai.py
```

or

```bash
python -m unittest test_ai.py
```

---

## How It Works

1. The game displays an empty 3×3 Tic-Tac-Toe board.
2. The human player selects a position for their move.
3. The AI evaluates all possible moves using the Minimax algorithm.
4. The AI chooses the move that maximizes its chance of winning while minimizing the opponent's chance.
5. The game continues until either player wins or the board is full, resulting in a draw.

---

## Minimax Algorithm

The AI uses the **Minimax algorithm**, a recursive search algorithm commonly used in two-player games.

### Evaluation Scores

* **+1** → AI wins
* **0** → Draw
* **−1** → Human wins

The algorithm recursively explores every possible game state and selects the move with the highest score, ensuring optimal play.

---

## Example Gameplay

```text
Current Board:

 X | O | X
-----------
 O | X |
-----------
   |   | O

Enter your move (1-9): 8

AI is thinking...

Current Board:

 X | O | X
-----------
 O | X |
-----------
   | O | O

AI wins!
```

---

## Learning Outcomes

This project helps you understand:

* Artificial Intelligence fundamentals.
* Game Theory concepts.
* Minimax search algorithm.
* Recursive programming.
* Decision-making in adversarial games.
* Python module organization.
* Writing and running unit tests.

---

## Future Enhancements

* Add Alpha-Beta Pruning to improve Minimax performance.
* Implement multiple difficulty levels.
* Develop a graphical user interface (GUI) using Tkinter or Pygame.
* Add score tracking and game statistics.
* Support online or local multiplayer mode.
* Improve board visualization and user experience.

---

## Conclusion

This project demonstrates how search algorithms can be applied to game-playing AI. By implementing the Minimax algorithm, the AI consistently selects the best possible move, making it an excellent introduction to Artificial Intelligence, game theory, and algorithmic problem-solving.
