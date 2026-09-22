

class Piece:
    def __init__(self, team, type, is_captured=False):
        self.team = team
        self.type = type
        self.is_captured = is_captured

class Board:
    def __init__(self):
        self.init_board_state = [
            [".", ".", ".", "A", "A", "A", "A", "A", ".", ".", "."],
            [".", ".", ".", ".", ".", "A", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["A", ".", ".", ".", ".", "D", ".", ".", ".", ".", "A"],
            ["A", ".", ".", ".", "D", "D", "D", ".", ".", ".", "A"],
            ["A", "A", ".", "D", "D", "C", "D", "D", ".", "A", "A"],
            ["A", ".", ".", ".", "D", "D", "D", ".", ".", ".", "A"],
            ["A", ".", ".", ".", ".", "D", ".", ".", ".", ".", "A"],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", "A", ".", ".", ".", ".", "."],
            [".", ".", ".", "A", "A", "A", "A", "A", ".", ".", "."]
        ]
        self.board_state  = []
        for row in self.init_board_state:
            row_items = []
            for square in row:
                if square == ".":
                    row_items.append(None)
                elif square == "A":
                    row_items.append(Piece("offense", "standard"))
                elif square == "D":
                    row_items.append(Piece("defense", "standard"))
                elif square == "C":
                    row_items.append(Piece("defense", "king"))
                self.board_state.append(row_items)
                




board = Board()
print(board.board_state)