

class Piece:
    VALID_TEAMS = ["offense", "defense"]
    VALID_TYPES = ["standard", "king"]

    def __init__(self, team, type="standard", is_captured=False):
        self.team = team
        self.type = type
        self.is_captured = is_captured

        # prevents invalid pieces
        if team not in self.VALID_TEAMS:
            raise ValueError(f"Invalid team '{team}'. Expected one of {self.VALID_TEAMS}")
        if type not in self.VALID_TYPES:
            raise ValueError(f"Invalid piece type '{type}'. Expected one of {self.VALID_TYPES}")
        if team == "offense" and type == "king":
            raise ValueError("Offense team cannot have a King piece.")

        
        #assigns text characters to pieces
        if self.team == "offense":
            self.character = "A"
        elif self.team == "defense" and self.type == "standard":
            self.character = "D"
        elif self.team == "defense" and self.type == "king":
            self.character = "K"

    def __str__(self):
        return self.character



class Board:
    VALID_COLUMNS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
    VALID_ROWS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    def __init__(self):
        self.turn = "offense"
        #Maps the peices on the board in a list. A = Offensive Piece, D = Defensive Piece, K = King Piece
        self.init_board_state = [
            [".", ".", ".", "A", "A", "A", "A", "A", ".", ".", "."],
            [".", ".", ".", ".", ".", "A", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["A", ".", ".", ".", ".", "D", ".", ".", ".", ".", "A"],
            ["A", ".", ".", ".", "D", "D", "D", ".", ".", ".", "A"],
            ["A", "A", ".", "D", "D", "K", "D", "D", ".", "A", "A"],
            ["A", ".", ".", ".", "D", "D", "D", ".", ".", ".", "A"],
            ["A", ".", ".", ".", ".", "D", ".", ".", ".", ".", "A"],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", "A", ".", ".", ".", ".", "."],
            [".", ".", ".", "A", "A", "A", "A", "A", ".", ".", "."]
        ]
        

        # Initializes piece classes into a 2D array as they appear on the board in the initial board position
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
                elif square == "K":
                    row_items.append(Piece("defense", "king"))
            self.board_state.append(row_items)
    def __str__(self):
        # Turns the board into a text string that can be printed for easy development
        board = " A B C D E F G H I J K\n"
        row_counter = 1
        for row in self.board_state:
            for square in row:
                if square is None:
                    board = f"{board} ."
                else:
                    board = f"{board} {square}"
            board = f"{board}  {row_counter}\n"
            row_counter += 1
        return board
    def translate_text_into_coorinate(self, coordinate_str):
        if len(coordinate_str) < 2:
            raise ValueError("Not a valid board square")
        column = coordinate_str.lower()[0]
        try:
            row = int(coordinate_str.lower()[1:])
        except ValueError as error:
            raise ValueError("Not a valid board square")
        if (column not in self.VALID_COLUMNS) or (row not in self.VALID_ROWS):
            raise ValueError("Not a valid board square")
        row -= 1
        column = self.VALID_COLUMNS.index(column)
        return (row, column)
        
    def translate_coorinate_into_text(self, coordinate):
        row, column = coordinate
        if (not 0 <= row <= 10) or (not 0 <= column <=10):
            raise ValueError("Invalid input")
        row = row + 1
        column = self.VALID_COLUMNS[column]

        return f"{column}{row}".upper()

    
    def select_board_square(self):
        pass
    def move_piece(self):
        pass
    def check_for_capture():
        pass


if __name__ == "__main__":

    board = Board()
    # text_board = board.print_board_state()
    print(board)