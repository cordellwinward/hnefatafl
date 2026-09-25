# Hnefatafl (Viking Chess) Game Engine

## Product Overview
**Hnefatafl** is an ancient Norse strategy board game featuring asymmetrical gameplay:
* **Attackers (Offense - 24 pieces):** Positioned along the outer board edges, working to capture the opposing King before he escapes[cite: 1, 2].
* **Defenders (Defense - 12 pieces + 1 King):** Positioned in the central formation surrounding the King, working to escort him safely to any of the four corner tiles[cite: 1, 2].

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

* **`Piece` Model:** Manages individual unit state, team affiliation (`offense` vs `defense`), type classification (`standard` vs `king`), and character mapping (`A`, `D`, `K`)[cite: 2].
* **`Board` Model:** Manages an $11 \times 11$ matrix populated with `Piece` instances and `None` placeholders[cite: 2]. Includes a built-in terminal display formatter for development[cite: 2].

---

## Current Status & Limitations

### Working Features
* **Matrix Setup:** $11 \times 11$ board state dynamically populated with `Piece` objects and empty space (`None`) markers[cite: 2].
* **CLI Rendering:** Terminal grid display using object string representations[cite: 2].

### Current Limitations (In Progress)
* **No Movement Logic Yet:** Pieces cannot yet select a target tile or validate orthogonal path clearance.
* **No Rules Engine Yet:** Capture detection (Custodian Capture) and King escape win conditions are pending implementation[cite: 1].
* **No Graphical UI:** Gameplay is currently restricted to terminal output while Pygame interface is under development[cite: 1].

---

## How to Run (Development CLI)

No external libraries are required at this stage in development. Run the script directly through standard Python:

```bash
python hnefatafl.py
```

### How to Run Tests

```bash
pytest -v