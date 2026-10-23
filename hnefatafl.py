import copy

class Piece:
    VALID_TEAMS = ["offense", "defense"]
    VALID_TYPES = ["standard", "king"]
    

    def __init__(self, team: str, piece_type: str = "standard") -> None:
        """Creates a piece for the specified team and piece type."""
        self.team = team
        self.piece_type = piece_type

        # prevents invalid pieces
        if team not in self.VALID_TEAMS:
            raise ValueError(f"Invalid team '{team}'. Expected one of {self.VALID_TEAMS}")
        if piece_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid piece type '{piece_type}'. Expected one of {self.VALID_TYPES}")
        if team == "offense" and piece_type == "king":
            raise ValueError("Offense team cannot have a King piece.")

        
        #assigns text characters to pieces
        if self.team == "offense":
            self.character = "A"
        elif self.team == "defense" and self.piece_type == "standard":
            self.character = "D"
        elif self.team == "defense" and self.piece_type == "king":
            self.character = "K"

    def __str__(self) -> str:
        """Returns the character used to display the piece."""
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
    BOARD_MAX_INDEX = 10 # For an 11x11 board including index 0
    
    
    def __init__(self) -> None:
        """Creates a board in the initial Hnefatafl position."""
        self.turn: str = "offense"
        self.game_over: bool = False
        self.victor: str = ""
        self.turns_without_capture: int = 0

        #Maps the pieces on the board in a list. A = Offensive Piece, D = Defensive Piece, K = King Piece
        self.init_board_state: list[list[str]] = [
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
        self.board_state: list[list[Piece | None]] = []
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
        self.board_state_history: list[list[list[Piece | None]]] = [copy.deepcopy(self.board_state)]

    def __str__(self) -> str:
        """Returns the board as a formatted text display."""
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
    
    def translate_text_into_coordinate(self, coordinate_str: str) -> tuple[int, int]:
        """Converts a board coordinate such as 'A1' into a row-column tuple."""
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
        
    def translate_coordinate_into_text(self, coordinate: tuple[int, int]) -> str:
        """Converts a row-column tuple into a board coordinate such as 'A1'."""
        row, column = coordinate
        if (not 0 <= row <= self.BOARD_MAX_INDEX) or (not 0 <= column <= self.BOARD_MAX_INDEX):
            raise ValueError("Invalid input")
        row = row + 1
        column = self.VALID_COLUMNS[column]

        return f"{column}{row}".upper()

    
    def select_board_square(self, coordinate: tuple[int, int]) -> list[tuple[int, int]] | None:
        """Returns the valid moves for the current team's piece at a square."""
        board_square = self.board_state[coordinate[self.BOARD_SQUARE_ROW_INX]][coordinate[self.BOARD_SQUARE_COLUMN_INX]]
        if board_square is None or board_square.team != self.turn:
            return None
        return self._find_valid_moves(coordinate)
        
        

    def _find_possible_paths(self, coordinate: tuple[int, int]) -> list[tuple[int, int]]:

        """Returns all squares in a unbroken path from
        a coordinate including the throne and corner squares."""

        possible_paths = []
        for direction in self.MOVEMENT_DIRECTIONS:
            row, column = direction
            square_around = (coordinate[self.BOARD_SQUARE_ROW_INX] + row, coordinate[self.BOARD_SQUARE_COLUMN_INX] + column)

            while (
                0 <= square_around[self.BOARD_SQUARE_ROW_INX] <= self.BOARD_MAX_INDEX
                and 0 <= square_around[self.BOARD_SQUARE_COLUMN_INX] <= self.BOARD_MAX_INDEX
                and self.board_state[square_around[self.BOARD_SQUARE_ROW_INX]][square_around[self.BOARD_SQUARE_COLUMN_INX]] is None
            ):
                possible_paths.append(square_around)
                square_around = (square_around[self.BOARD_SQUARE_ROW_INX] + row, square_around[self.BOARD_SQUARE_COLUMN_INX] + column)
        return possible_paths

    def _find_valid_moves(self, coordinate: tuple[int, int])-> list[tuple[int, int]] | None:
        """Finds and returns all valid moves a square can make without validating whose turn it is"""
        board_square = self.board_state[coordinate[self.BOARD_SQUARE_ROW_INX]][coordinate[self.BOARD_SQUARE_COLUMN_INX]]
        if board_square is None:
            return None
        valid_moves = self._find_possible_paths(coordinate)
        if board_square.piece_type == "standard":
            if self.THRONE_SQUARE in valid_moves:
                valid_moves.remove(self.THRONE_SQUARE)
            for corner in self.CORNER_SQUARES:
                if corner in valid_moves:
                    valid_moves.remove(corner)
        
        return valid_moves
        


    def move_piece(self, move_from: tuple[int, int], move_to: tuple[int, int]) -> None:
        """Moves a piece, updates board history, resolves captures, checks for game-ending conditions, and switches turns."""
        if (
            not 0 <= move_from[self.BOARD_SQUARE_ROW_INX] <= self.BOARD_MAX_INDEX
            or not 0 <= move_from[self.BOARD_SQUARE_COLUMN_INX] <= self.BOARD_MAX_INDEX
        ):
            raise ValueError("move_from is outside the board")
        if (
            not 0 <= move_to[self.BOARD_SQUARE_ROW_INX] <= self.BOARD_MAX_INDEX
            or not 0 <= move_to[self.BOARD_SQUARE_COLUMN_INX] <= self.BOARD_MAX_INDEX
        ):
            raise ValueError("move_to is outside the board")
        if self.board_state[move_from[self.BOARD_SQUARE_ROW_INX]][move_from[self.BOARD_SQUARE_COLUMN_INX]] is None:
            raise ValueError("move_from does not contain a piece")
        if self.board_state[move_from[self.BOARD_SQUARE_ROW_INX]][move_from[self.BOARD_SQUARE_COLUMN_INX]].team != self.turn:
            raise ValueError("move_from piece cannot move since it is not its team's turn")
        if self.board_state[move_to[self.BOARD_SQUARE_ROW_INX]][move_to[self.BOARD_SQUARE_COLUMN_INX]] is not None:
            raise ValueError("move_to is occupied")
        if move_to not in self._find_valid_moves(move_from):
            raise ValueError("That is not a valid move")
        
        piece = self.board_state[move_from[self.BOARD_SQUARE_ROW_INX]][move_from[self.BOARD_SQUARE_COLUMN_INX]]
        self.board_state[move_from[self.BOARD_SQUARE_ROW_INX]][move_from[self.BOARD_SQUARE_COLUMN_INX]] = None
        self.board_state[move_to[self.BOARD_SQUARE_ROW_INX]][move_to[self.BOARD_SQUARE_COLUMN_INX]] = piece
        captured_pieces_team = self._check_for_capture(move_to)
        self._check_for_game_end_conditions(move_to, captured_pieces_team)
        self.board_state_history.append(copy.deepcopy(self.board_state))

        #Change turns
        if self.turn == "offense":
            self.turn = "defense"
        elif self.turn == "defense":
            self.turn = "offense"



    def _check_for_capture(self, move_to: tuple[int, int]) -> str | None:
        """Checks whether a move captured an opposing piece."""
        captured_team = None
        piece = self.board_state[move_to[self.BOARD_SQUARE_ROW_INX]][move_to[self.BOARD_SQUARE_COLUMN_INX]]
        for row, column in self.MOVEMENT_DIRECTIONS:
            square_around = ((move_to[self.BOARD_SQUARE_ROW_INX] + row), (move_to[self.BOARD_SQUARE_COLUMN_INX] + column))
            if (
                not 0 <= square_around[self.BOARD_SQUARE_ROW_INX] <= self.BOARD_MAX_INDEX
                or not 0 <= square_around[self.BOARD_SQUARE_COLUMN_INX] <= self.BOARD_MAX_INDEX
            ):
                continue
            square_around_piece = self.board_state[square_around[self.BOARD_SQUARE_ROW_INX]][square_around[self.BOARD_SQUARE_COLUMN_INX]]
            
            if square_around_piece is not None and square_around_piece.team != piece.team:
                capturing_square = (square_around[self.BOARD_SQUARE_ROW_INX] + row, square_around[self.BOARD_SQUARE_COLUMN_INX] + column)
                if (
                    not 0 <= capturing_square[self.BOARD_SQUARE_ROW_INX] <= self.BOARD_MAX_INDEX
                    or not 0 <= capturing_square[self.BOARD_SQUARE_COLUMN_INX] <= self.BOARD_MAX_INDEX
                ):
                    continue
                capturing_square_piece = self.board_state[capturing_square[self.BOARD_SQUARE_ROW_INX]][capturing_square[self.BOARD_SQUARE_COLUMN_INX]]
                
                if (
                    capturing_square_piece is None
                    and capturing_square not in self.CORNER_SQUARES
                    and capturing_square != self.THRONE_SQUARE
                ):
                    pass
                elif (capturing_square in self.CORNER_SQUARES or
                    (capturing_square == self.THRONE_SQUARE and
                    self.board_state[self.THRONE_SQUARE[self.BOARD_SQUARE_ROW_INX]][self.THRONE_SQUARE[self.BOARD_SQUARE_COLUMN_INX]] is None) or
                    capturing_square_piece.team == piece.team):
                    
                    match square_around_piece.piece_type:
                        
                        case "standard":
                            self.board_state[square_around[self.BOARD_SQUARE_ROW_INX]][square_around[self.BOARD_SQUARE_COLUMN_INX]] = None
                            captured_team = square_around_piece.team
                        case "king":
                            self._capture_king(square_around)
        return captured_team

    def _capture_king(self, kings_square: tuple[int, int]) -> None:
        """Checks whether the king is surrounded and ends the game if captured."""
        king_row, king_column = kings_square
        num_attacking_pieces = 0
        for row, column in self.MOVEMENT_DIRECTIONS:
            square_around = (king_row + row, king_column + column)
            if (
                not 0 <= square_around[self.BOARD_SQUARE_ROW_INX] <= self.BOARD_MAX_INDEX
                or not 0 <= square_around[self.BOARD_SQUARE_COLUMN_INX] <= self.BOARD_MAX_INDEX
            ):
                break
            square_around_piece = self.board_state[square_around[self.BOARD_SQUARE_ROW_INX]][square_around[self.BOARD_SQUARE_COLUMN_INX]]
            if (square_around == self.THRONE_SQUARE or
                (square_around_piece is not None
                 and square_around_piece.team == "offense")):
                num_attacking_pieces += 1
            else:
                break
        if num_attacking_pieces == 4:
            self.game_over = True
            self.victor = "offense"
        

        
    def _check_for_game_end_conditions(
        self,
        moved_to_square: tuple[int, int],
        captured_pieces_team: str | None,
    ) -> None:
        """Checks whether the latest move ended the game."""
        if self._check_for_50_turns_without_capture(captured_pieces_team):
            self.game_over = True
            self.victor = "draw"
        if not self._check_for_possible_moves():
            self.game_over = True
            self.victor = self.turn
        if self.turn == "offense":
            if self._check_for_encircled_defenders(moved_to_square, captured_pieces_team):
                self.game_over = True
                self.victor = "offense"
        if self.turn == "defense":
            if self._check_for_king_in_corner():
                self.game_over = True
                self.victor = "defense"

    def _check_for_50_turns_without_capture(self, captured_piece_team: str | None) -> bool:
        """Checks to see if 50 complete turns (1 turn for offense, 1 for defense) have occurred
        without any captures. If so returns True. Otherwise returns False"""
        if captured_piece_team == "offense" or captured_piece_team == "defense":
            self.turns_without_capture = 0
        elif captured_piece_team is None:
            self.turns_without_capture += 1
        if self.turns_without_capture >= 100:
            return True
        else:
            return False

    def _check_for_king_in_corner(self) -> bool:
        """Checks to see if the King escaped the board to the corner. Returns True if the king is on a corner square. False otherwise."""
        match self.turn:
            case "offense":
                return False
            case "defense":
                for square in self.CORNER_SQUARES:
                    row, column = square
                    square_piece = self.board_state[row][column]
                    if square_piece is not None:
                        return True
                return False

    def find_all_pieces_of_team(self, team: str) -> list[tuple[int, int]]:
        """Returns the board coordinates of every piece on a team."""
        piece_locations = []
        row_inx = 0
        for row in self.board_state:
            column_inx = 0
            for column in row:
                if column is not None and column.team == team:
                    piece_locations.append((row_inx, column_inx))
                column_inx += 1
            row_inx += 1
        return piece_locations
    
    def _check_for_encircled_defenders(
        self,
        moved_to_square: tuple[int, int],
        captured_pieces_team: str | None,
    ) -> bool:
        """Checks whether the defenders have been completely encircled."""
        if (captured_pieces_team == "defense" 
        or self._check_for_2_pieces_of_team_next_to_square(moved_to_square, "defense")):
            return self._run_algorithm_for_encircled_defenders()
        return False
        
    def _run_algorithm_for_encircled_defenders(self) -> bool:
        """Runs full algorithm to check if defenders completely encircled. Returns False if defenders not completely encircled. True if they are."""
        defensive_squares = self.find_all_pieces_of_team("defense")
        checked_squares = set()
        for square in defensive_squares:
            row, column = square
            if row in [self.BOARD_MAX_INDEX, 0] or column in [self.BOARD_MAX_INDEX, 0]:
                return False
            if not self._run_algorithm_for_encircled_defenders_recursion(square,checked_squares):
                return False
        return True

    def _run_algorithm_for_encircled_defenders_recursion(
        self,
        square: tuple[int, int],
        checked_squares: set[tuple[int, int]],
    ) -> bool:
        """Checks recursively whether defenders can reach an unencircled square."""
        possible_paths = self._find_possible_paths(square)
        for next_square in possible_paths:
            if next_square in checked_squares:
                continue
            checked_squares.add(next_square)
            row, column = next_square
            if row in [self.BOARD_MAX_INDEX, 0] or column in [self.BOARD_MAX_INDEX, 0]:
                return False
            if not self._run_algorithm_for_encircled_defenders_recursion(next_square, checked_squares):
                return False
        return True
    
    def _check_for_2_pieces_of_team_next_to_square(
        self,
        square: tuple[int, int],
        team: str,
    ) -> bool:
        """Checks for 2 or more pieces of the passed team next to a passed square."""
        row, column = square
        num_of_adjacent_pieces = 0
        for adjacent_row, adjacent_column in self.ALL_ADJACENT_SQUARES:
            adjacent_row += row
            adjacent_column += column
            if not (0 <= adjacent_row <= self.BOARD_MAX_INDEX) or not (0 <= adjacent_column <= self.BOARD_MAX_INDEX):
                continue
            if (self.board_state[adjacent_row][adjacent_column] is not None
                and self.board_state[adjacent_row][adjacent_column].team == team):
                num_of_adjacent_pieces += 1
        if num_of_adjacent_pieces >= 2:
            return True
        else:
            return False


    def _check_for_possible_moves(self) -> bool:
        """Checks whether the next team has any legal moves."""
        match self.turn:
            case "offense":
                team = "defense"
            case "defense":
                team = "offense"
        pieces = self.find_all_pieces_of_team(team)
        for piece in pieces:
            if self._find_valid_moves(piece):
                return True
        return False
                         
                    





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
            if valid_moves is None:
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
    print(f"Game Over. {board.victor.capitalize()} wins.")
