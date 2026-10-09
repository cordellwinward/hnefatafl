# Hnefatafl (Viking Chess) Game Engine

## Product Overview
**Hnefatafl** is an ancient Norse strategy board game featuring asymmetrical gameplay:
* **Attackers (Offense - 24 pieces):** Positioned along the outer board edges, working to capture the opposing King before he escapes.
* **Defenders (Defense - 12 pieces + 1 King):** Positioned in the central formation surrounding the King, working to escort him safely to any of the four corner tiles.

All pieces move orthogonally across unobstructed paths, capturing opposing pieces through **Custodian Capture** (sandwiching an enemy piece between two of your own).

---

## Tech Stack
* **Core Language:** Python 3
* **Testing** Pytest
* **Graphical Interface (Planned):** Pygame
* **Future Stack:** SQL, HTML, CSS, JavaScript (for planned web version)

---

## Software Architecture Overview

The system is built around an Object-Oriented paradigm with two core entities:

* **`Piece` Model:** Manages individual unit state, team affiliation (`offense` vs `defense`), type classification (`standard` vs `king`), and character mapping (`A`, `D`, `K`).
* **`Board` Model:** Manages an $11 \times 11$ matrix populated with `Piece` instances and `None` placeholders. Includes a built-in terminal display formatter for development.

---

## Current Status & Limitations

### Working Features
* **Matrix Setup:** $11 \times 11$ board state dynamically populated with `Piece` objects and empty space (`None`) markers.
* **CLI Rendering:** Terminal grid display using object string representations.
* **Coordinate Conversion:** Conversion between text coordinates such as `A1` and zero-based board coordinates.
* **Move Selection:** Selection of orthogonal, unobstructed destinations for the current team's pieces, including restrictions for standard pieces on corner and throne squares.
* **Piece Movement:** Pieces can be moved between valid board squares, turns alternate between offense and defense, and previous board states are tracked.
* **Partial Capture Detection:** Standard opposing pieces can be removed through supported Custodian Capture situations.

### Current Limitations (In Progress)
* **Move Execution Validation:** `move_piece` does not independently validate that its source and destination coordinates represent a legal move; callers should use the move-selection logic first.
* **Incomplete Rules Engine:** King capture, King escape, and game-over/victor state handling are not yet implemented.
* **No Graphical UI:** Gameplay is currently restricted to terminal output while Pygame interface is under development.

---

## How to Run (Development CLI)

No external libraries are required at this stage in development. Run the script directly through standard Python:

```bash
python hnefatafl.py
```

### How to Run Tests

```bash
pytest -v
