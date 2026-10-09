import copy

class Piece:
    VALID_TEAMS = ["offense", "defense"]
    VALID_TYPES = ["standard", "king"]
    

    def __init__(self, team, type="standard"):
        self.team = team
        self.type = type

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
    BOARD_SQUARE_ROW_INX = 0
    BOARD_SQUARE_COLUMN_INX = 1
    MOVEMENT_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    ALL_ADJACENT_SQUARES = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    CORNER_SQUARES = [(0, 0), (0, 10), (10, 0), (10, 10)]
    THRONE_SQUARE = (5, 5)
    
    
    def __init__(self):
        self.turn = "offense"
        self.game_over = False
        self.victor = ""
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
        self.board_state_history = [copy.deepcopy(self.board_state)]

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
    
    def translate_text_into_coordinate(self, coordinate_str):
        if len(coordinate_str.strip()) < 2:
            raise ValueError("Not a valid board square")
        column = coordinate_str.lower()[0]
        try:
            row = int(coordinate_str.lower().strip()[1:])
        except ValueError as error:
            raise ValueError("Not a valid board square")
        if (column not in self.VALID_COLUMNS) or (row not in self.VALID_ROWS):
            raise ValueError("Not a valid board square")
        row -= 1
        column = self.VALID_COLUMNS.index(column)
        return (row, column)
        
    def translate_coordinate_into_text(self, coordinate):
        row, column = coordinate
        if (not 0 <= row <= 10) or (not 0 <= column <=10):
            raise ValueError("Invalid input")
        row = row + 1
        column = self.VALID_COLUMNS[column]

        return f"{column}{row}".upper()

    
    def select_board_square(self, coordinate: tuple[int, int]) -> list[tuple[int, int]] | None:
        board_square = self.board_state[coordinate[self.BOARD_SQUARE_ROW_INX]][coordinate[self.BOARD_SQUARE_COLUMN_INX]]
        if board_square == None or board_square.team != self.turn:
            return None
        
        
        valid_moves = []
        for direction in self.MOVEMENT_DIRECTIONS:
            row, column = direction
            square_around = (coordinate[self.BOARD_SQUARE_ROW_INX] + row, coordinate[self.BOARD_SQUARE_COLUMN_INX] + column)

            while (
                (square_around[self.BOARD_SQUARE_ROW_INX] >= 0 and square_around[self.BOARD_SQUARE_ROW_INX] <= 10)
                and (square_around[self.BOARD_SQUARE_COLUMN_INX] >= 0 
                and square_around[self.BOARD_SQUARE_COLUMN_INX] <= 10) 
                and (self.board_state[square_around[self.BOARD_SQUARE_ROW_INX]][square_around[self.BOARD_SQUARE_COLUMN_INX]] == None)
                ):
                valid_moves.append(square_around)
                square_around = (square_around[self.BOARD_SQUARE_ROW_INX] + row, square_around[self.BOARD_SQUARE_COLUMN_INX] + column)
        if board_square.type == "standard":
            if self.THRONE_SQUARE in valid_moves:
                valid_moves.remove(self.THRONE_SQUARE)
            for corner in self.CORNER_SQUARES:
                if corner in valid_moves:
                    valid_moves.remove(corner)
        
        return valid_moves
        



    def move_piece(self, move_from: tuple[int, int], move_to: tuple[int, int]):
        piece = self.board_state[move_from[self.BOARD_SQUARE_ROW_INX]][move_from[self.BOARD_SQUARE_COLUMN_INX]]
        self.board_state[move_from[self.BOARD_SQUARE_ROW_INX]][move_from[self.BOARD_SQUARE_COLUMN_INX]] = None
        self.board_state[move_to[self.BOARD_SQUARE_ROW_INX]][move_to[self.BOARD_SQUARE_COLUMN_INX]] = piece
        self.board_state_history.append(copy.deepcopy(self.board_state))
        self.check_for_capture(move_to)

        #Change turns
        if self.turn == "offense":
            self.turn = "defense"
        elif self.turn == "defense":
            self.turn = "offense"



    def check_for_capture(self, move_to: tuple[int, int]):
        piece = self.board_state[move_to[self.BOARD_SQUARE_ROW_INX]][move_to[self.BOARD_SQUARE_COLUMN_INX]]
        for row, column in self.MOVEMENT_DIRECTIONS:
            square_around = ((move_to[self.BOARD_SQUARE_ROW_INX] + row), (move_to[self.BOARD_SQUARE_COLUMN_INX] + column))
            if not (0 <= square_around[self.BOARD_SQUARE_ROW_INX] <= 10) or not (0 <= square_around[self.BOARD_SQUARE_COLUMN_INX] <= 10):
                continue
            square_around_piece = self.board_state[square_around[self.BOARD_SQUARE_ROW_INX]][square_around[self.BOARD_SQUARE_COLUMN_INX]]
            
            if square_around_piece is not None and square_around_piece.team != piece.team:
                capturing_square = (square_around[self.BOARD_SQUARE_ROW_INX] + row, square_around[self.BOARD_SQUARE_COLUMN_INX] + column)
                if not (0 <= capturing_square[self.BOARD_SQUARE_ROW_INX] <= 10) or not (0 <= capturing_square[self.BOARD_SQUARE_COLUMN_INX] <= 10):
                    continue
                capturing_square_piece = self.board_state[capturing_square[self.BOARD_SQUARE_ROW_INX]][capturing_square[self.BOARD_SQUARE_COLUMN_INX]] 
                
                if capturing_square_piece is None and capturing_square not in self.CORNER_SQUARES and capturing_square != self.THRONE_SQUARE:
                    pass
                elif (capturing_square in self.CORNER_SQUARES or
                    (capturing_square == self.THRONE_SQUARE and
                    self.board_state[self.THRONE_SQUARE[self.BOARD_SQUARE_ROW_INX]][self.THRONE_SQUARE[self.BOARD_SQUARE_COLUMN_INX]] is None) or
                    capturing_square_piece.team == piece.team):
                    
                    match square_around_piece.type:
                        
                        case "standard":
                            self.board_state[square_around[self.BOARD_SQUARE_ROW_INX]][square_around[self.BOARD_SQUARE_COLUMN_INX]] = None
                        case "king":
                            self.capture_king()

    def capture_king(self):
        pass

        
    def check_for_game_end_conditions(self):
        pass                                
                    




if __name__ == "__main__":

    board = Board()
    print(board)
    while board.game_over != True:
        is_valid_move = False
        valid_moves = None
        while valid_moves is None or valid_moves == []:
            try:
                move_from = input("Where would you like to move from? ")
                coordinate_from = board.translate_text_into_coordinate(move_from)
            except ValueError:
                print("Invalid input. Please enter a valid board square such as 'A1'.")
                continue
            valid_moves = board.select_board_square(coordinate_from)
            if valid_moves == None:
                print("You have no pieces on this tile.")
            elif valid_moves == []:
                print("This piece has no possible moves")
        while is_valid_move == False:
            try:
                move_to = input("Where would you like to move to? (Enter 'back' to choose new piece to move) ")
                if move_to.lower().strip() == "back":
                    break
                coordinate_to = board.translate_text_into_coordinate(move_to)
            except ValueError:
                print("Invalid input. Please enter a valid board square such as 'A1'.")
                continue
            if coordinate_to in valid_moves:
                board.move_piece(coordinate_from, coordinate_to)
                is_valid_move = True
                print(board)
            else:
                print("That move is invalid. Please make a valid move")