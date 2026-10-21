import pytest
from hnefatafl import Board, Piece


def test_piece_init():
    offense = Piece("offense", "standard")
    assert offense.type == "standard"
    assert offense.team == "offense"
    assert offense.character == "A"

    defense = Piece("defense")
    assert defense.type == "standard"
    assert defense.team == "defense"
    assert defense.character == "D"
    king = Piece("defense", type="king")
    assert king.type == "king"
    assert king.team == "defense"
    assert king.character == "K"

    with pytest.raises(ValueError):
        Piece("neutral")

    with pytest.raises(ValueError):
        Piece("offense", type="wizard")

    with pytest.raises(ValueError):
        Piece(team="offense", type="king")


def test_piece_str():
    offense = Piece("offense")
    defense = Piece("defense")
    king = Piece("defense", type="king")

    # Verify __str__ returns the correct character string
    assert str(offense) == "A"
    assert str(defense) == "D"
    assert str(king) == "K"
    
    

def test_board_init():
    board = Board()
    
    # 1. Test Matrix Dimensions
    assert len(board.board_state) == 11
    assert all(len(row) == 11 for row in board.board_state)
    
    # 2. Test Specific Piece Positions
    assert board.board_state[5][5].type == "king"  # King on F6
    assert board.board_state[0][5].team == "offense"  # Attacker on F1
    assert board.board_state[4][5].team == "defense"  # Defender on F5
    
    # 3. Test Empty Spaces
    assert board.board_state[0][0] is None  # Corners start empty
    assert board.board_state[1][1] is None  # Non-starting tile is empty
    
    # 4. Test Game Tracking Attributes
    assert board.turn == "offense"

def test_board_str():
    board = Board()
    
    expected_output = (
        " A B C D E F G H I J K\n"
        " . . . A A A A A . . .  1\n"
        " . . . . . A . . . . .  2\n"
        " . . . . . . . . . . .  3\n"
        " A . . . . D . . . . A  4\n"
        " A . . . D D D . . . A  5\n"
        " A A . D D K D D . A A  6\n"
        " A . . . D D D . . . A  7\n"
        " A . . . . D . . . . A  8\n"
        " . . . . . . . . . . .  9\n"
        " . . . . . A . . . . .  10\n"
        " . . . A A A A A . . .  11\n"
    )
    assert str(board) == expected_output

def test_translate_text_into_coordinate():
    board = Board()
    assert board.translate_text_into_coordinate("A4") == (3, 0)
    assert board.translate_text_into_coordinate("K11") == (10, 10)
    assert board.translate_text_into_coordinate("h5") == (4, 7)

    with pytest.raises(ValueError):
        board.translate_text_into_coordinate ("L10")
    with pytest.raises(ValueError):
        board.translate_text_into_coordinate("A13")
    with pytest.raises(ValueError):
        board.translate_text_into_coordinate("A")
    with pytest.raises(ValueError):
        board.translate_text_into_coordinate("AB")
    with pytest.raises(ValueError):
        board.translate_text_into_coordinate("A1C")

def test_translate_coordinate_into_text():
    board = Board()
    assert board.translate_coordinate_into_text((3, 0)) == "A4"
    assert board.translate_coordinate_into_text((10, 10)) == "K11"
    assert board.translate_coordinate_into_text((4, 7)) == "H5"

    with pytest.raises(ValueError):
        board.translate_coordinate_into_text((-1, 0))
    with pytest.raises(ValueError):
        board.translate_coordinate_into_text((0, -1))
    with pytest.raises(ValueError):
        board.translate_coordinate_into_text((11, 0))
    with pytest.raises(ValueError):
        board.translate_coordinate_into_text((0, 11))

def test_select_board_square():
    board = Board()
    assert board.select_board_square((0, 3)) == [(0, 2), (0, 1), (1, 3), (2, 3), (3, 3), (4, 3)]
    assert board.select_board_square((3, 0)) == [(3, 1), (3, 2), (3, 3), (3, 4), (2, 0), (1, 0)]
    assert board.select_board_square((5, 0)) == []
    assert board.select_board_square((2, 2)) is None

    board.turn = "defense"
    assert board.select_board_square((5, 3)) == [(5, 2), (4, 3), (3, 3), (2, 3), (1, 3), (6, 3), (7, 3), (8, 3), (9, 3)]
    assert board.select_board_square((5, 5)) == []
    assert board.select_board_square((0, 3)) is None


def test_find_possible_paths_stops_at_pieces():
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.board_state[5][5] = Piece("offense")
    board.board_state[5][2] = Piece("defense")
    board.board_state[5][8] = Piece("defense")
    board.board_state[2][5] = Piece("defense")
    board.board_state[8][5] = Piece("defense")

    assert board._find_possible_paths((5, 5)) == [
        (5, 4), (5, 3),
        (5, 6), (5, 7),
        (4, 5), (3, 5),
        (6, 5), (7, 5),
    ]


def test_find_valid_moves_for_standard_piece():
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]

    board.board_state[5][4] = Piece("offense")
    standard_moves = board._find_valid_moves((5, 4))
    assert board.THRONE_SQUARE not in standard_moves

    board.board_state[0][1] = Piece("offense")
    standard_moves = board._find_valid_moves((0, 1))
    assert (0, 0) not in standard_moves
    assert (0, 2) in standard_moves

    assert board._find_valid_moves((0, 0)) is None


def test_find_valid_moves_for_king_includes_special_squares():
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]

    board.board_state[5][4] = Piece("defense", type="king")
    assert board.THRONE_SQUARE in board._find_valid_moves((5, 4))

    board.board_state[0][1] = Piece("defense", type="king")
    assert (0, 0) in board._find_valid_moves((0, 1))


def test_move_piece():

    board = Board()
    board.move_piece((0, 3), (0, 1))
    assert board.board_state[0][3] is None
    assert board.board_state[0][1].team == "offense"
    assert board.turn == "defense"
    assert len(board.board_state) == 11
    assert len(board.board_state[0]) == 11
    assert len(board.board_state_history) == 2

    board.move_piece((5, 3), (2, 3))
    assert board.board_state[5][3] is None
    assert board.board_state[2][3].team == "defense"
    assert board.turn == "offense"
    assert len(board.board_state) == 11
    assert len(board.board_state[5]) == 11
    assert len(board.board_state_history) == 3


def test_move_piece_rejects_invalid_moves():
    board = Board()

    with pytest.raises(ValueError, match="move_from is outside the board"):
        board.move_piece((-1, 3), (0, 3))

    with pytest.raises(ValueError, match="move_to is outside the board"):
        board.move_piece((0, 3), (0, 11))

    with pytest.raises(ValueError, match="move_from does not contain a piece"):
        board.move_piece((2, 2), (2, 3))

    with pytest.raises(ValueError, match="not its team's turn"):
        board.move_piece((5, 5), (5, 4))

    with pytest.raises(ValueError, match="move_to is occupied"):
        board.move_piece((0, 3), (0, 4))

    with pytest.raises(ValueError, match="not a valid move"):
        board.move_piece((0, 3), (1, 4))


def test_move_piece_integration():
    # Verify that move_piece() triggers capture handling.
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][5] = Piece("defense")
    board.board_state[4][4] = Piece("defense")
    board.board_state[5][6] = Piece("offense")
    board.board_state[5][2] = Piece("offense")

    board.move_piece((5, 2), (5, 4))

    assert board.board_state[5][4].team == "offense"
    assert board.board_state[5][5] is None

    # Verify that encirclement through move_piece() ends the game.
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][5] = Piece("defense")
    board.board_state[5][6] = Piece("offense")
    board.board_state[5][2] = Piece("offense")

    board.move_piece((5, 2), (5, 4))

    assert board.game_over
    assert board.victor == "offense"

    # Verify that an ordinary move does not end the game.
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][8] = Piece("offense")
    board.board_state[4][4] = Piece("defense")

    board.move_piece((5, 8), (5, 7))

    assert not board.game_over
    assert board.victor == ""


def test_check_for_capture_corners():
    #Corner Captures
    board = Board()

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[0][1] = Piece("defense")
    board.board_state[0][2] = Piece("offense")
    captured_team = board.check_for_capture((0, 2))
    assert captured_team == "defense"
    assert board.board_state[0][1] is None
    assert board.board_state[0][2].team == "offense"

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[0][9] = Piece("offense")
    board.board_state[0][8] = Piece("defense")
    captured_team = board.check_for_capture((0, 8))
    assert captured_team == "offense"
    assert board.board_state[0][9] is None


    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[10][1] = Piece("defense")
    board.board_state[10][2] = Piece("offense")
    captured_team = board.check_for_capture((10, 2))
    assert captured_team == "defense"
    assert board.board_state[10][1] is None
    
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[10][9] = Piece("offense")
    board.board_state[10][8] = Piece("defense")
    captured_team = board.check_for_capture((10, 8))
    assert captured_team == "offense"
    assert board.board_state[10][9] is None

def test_check_for_capture_edges():
    # Board Edges & Boundary Safety (Indices 0, 10, 1, and 9)
    board = Board()

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[4][0] = Piece("defense")
    board.board_state[5][0] = Piece("offense")
    board.board_state[6][0] = Piece("defense")
    captured_team = board.check_for_capture((6, 0))
    assert captured_team == "offense"
    assert board.board_state[5][0] is None

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[0][4] = Piece("defense")
    board.board_state[0][5] = Piece("offense")
    board.board_state[0][6] = Piece("defense")
    captured_team = board.check_for_capture((0, 6))
    assert captured_team == "offense"
    assert board.board_state[0][5] is None
    
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][0] = Piece("defense")
    board.board_state[5][10] = Piece("offense")
    board.board_state[5][1] = Piece("offense")
    captured_team = board.check_for_capture((5, 1))
    assert captured_team is None
    assert board.board_state[5][0].team == "defense"
    

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][10] = Piece("defense")
    board.board_state[5][9] = Piece("offense")
    captured_team = board.check_for_capture((5, 9))
    assert captured_team is None
    assert board.board_state[5][10].team == "defense"

def test_check_for_capture_throne():
    #Throne Hostility
    board = Board()    

    #empty throne
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[5][6] = Piece("offense")
    board.board_state[5][7] = Piece("defense")
    captured_team = board.check_for_capture((5, 7))
    assert captured_team == "offense"
    assert board.board_state[5][6] is None

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][5] = Piece("defense", type="king")
    board.board_state[5][6] = Piece("defense")
    board.board_state[5][7] = Piece("offense")
    captured_team = board.check_for_capture((5, 7))
    assert captured_team is None
    assert board.board_state[5][6].team == "defense"

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[5][5] = Piece("defense", type="king")
    board.board_state[5][6] = Piece("offense")
    board.board_state[5][7] = Piece("defense")
    captured_team = board.check_for_capture((5, 7))
    assert captured_team == "offense"
    assert board.board_state[5][6] is None

def test_check_for_capture_special():
    #King not captured by 2 pieces
    board = Board()

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[3][2] = Piece("offense")
    board.board_state[3][3] = Piece("defense", type="king")
    board.board_state[3][4] = Piece("offense")
    captured_team = board.check_for_capture((3, 4))
    assert captured_team is None
    assert board.board_state[3][3].type == "king"

    #Multi-Capture
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][7] = Piece("offense")
    board.board_state[6][7] = Piece("defense")
    board.board_state[7][7] = Piece("offense")
    board.board_state[7][8] = Piece("defense")
    board.board_state[7][9] = Piece("offense")
    captured_team = board.check_for_capture((7, 7))
    assert captured_team == "defense"
    assert board.board_state[6][7] is None
    assert board.board_state[7][8] is None

    #Isn't captured when moving between hostile pieces
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[7][2] = Piece("defense")
    board.board_state[7][3] = Piece("offense")
    board.board_state[7][4] = Piece("defense")
    captured_team = board.check_for_capture((7, 3))
    assert captured_team is None
    assert board.board_state[7][3].team == "offense"

    #Can't capture friendly pieces
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[7][2] = Piece("defense")
    board.board_state[7][3] = Piece("defense")
    board.board_state[7][4] = Piece("defense")
    captured_team = board.check_for_capture((7, 2))
    assert captured_team is None
    assert board.board_state[7][3].team == "defense"

def test_capture_king():
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][5] = Piece("defense", type = "king")
    board.board_state[5][4] = Piece("offense")
    board.board_state[4][5] = Piece("offense")
    board.board_state[6][5] = Piece("offense")
    board.board_state[5][6] = Piece("offense")
    board.capture_king((5, 5))
    assert board.game_over == True
    assert board.victor == "offense"

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][4] = Piece("defense", type = "king")
    board.board_state[5][3] = Piece("offense")
    board.board_state[4][4] = Piece("offense")
    board.board_state[6][4] = Piece("offense")
    board.capture_king((5, 4))
    assert board.game_over == True
    assert board.victor == "offense"

    board.game_over = False
    board.victor = ""
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[0][5] = Piece("defense", type = "king")
    board.board_state[0][4] = Piece("offense")
    board.board_state[0][6] = Piece("offense")
    board.board_state[1][5] = Piece("offense")
    # Ensure an off-board direction does not wrap to the opposite board edge.
    board.board_state[-1][5] = Piece("offense")
    board.capture_king((0, 5))
    assert board.game_over == False
    assert board.victor == ""

    board.game_over = False
    board.victor = ""
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][10] = Piece("defense", type="king")
    board.board_state[5][9] = Piece("offense")
    board.capture_king((5, 10))   # IndexError before the fix
    assert board.game_over == False
    assert board.victor == ""

def test_check_for_king_in_corner():
    board = Board()

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[0][0] = Piece("defense", type = "king")
    board._check_for_king_in_corner()
    assert board.game_over == True
    assert board.victor == "defense"

    board.game_over = False
    board.victor = ""
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[10][10] = Piece("defense", type = "king")
    board._check_for_king_in_corner()
    assert board.game_over == True
    assert board.victor == "defense"

    board.game_over = False
    board.victor = ""
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[4][4] = Piece("defense", type = "king")
    board._check_for_king_in_corner()
    assert board.game_over == False
    assert board.victor == ""

    board.game_over = False
    board.victor = ""
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[10][10] = Piece("defense", type = "king")
    board._check_for_king_in_corner()
    assert board.game_over == False
    assert board.victor == ""

def test_find_all_pieces_of_team():
    board = Board()

    assert board.find_all_pieces_of_team("defense") == [
        (3, 5),
        (4, 4), (4, 5), (4, 6),
        (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
        (6, 4), (6, 5), (6, 6),
        (7, 5),
    ]

    assert board.find_all_pieces_of_team("offense") == [
        (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        (1, 5),
        (3, 0), (3, 10),
        (4, 0), (4, 10),
        (5, 0), (5, 1), (5, 9), (5, 10),
        (6, 0), (6, 10),
        (7, 0), (7, 10),
        (9, 5),
        (10, 3), (10, 4), (10, 5), (10, 6), (10, 7),
    ]


def test_run_algorithm_for_encircled_defenders():
    # A defender on the edge is not encircled.
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.board_state[0][5] = Piece("defense")

    assert board._run_algorithm_for_encircled_defenders() is False

    # Defenders enclosed by opposing pieces are encircled.
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.board_state[5][5] = Piece("defense")
    board.board_state[4][4] = Piece("defense")

    for column in range(3, 8):
        board.board_state[3][column] = Piece("offense")
        board.board_state[7][column] = Piece("offense")

    for row in range(4, 7):
        board.board_state[row][3] = Piece("offense")
        board.board_state[row][7] = Piece("offense")

    assert board._run_algorithm_for_encircled_defenders() is True

    # An open path to the edge means the defenders are not encircled.
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.board_state[5][5] = Piece("defense")
    board.board_state[5][4] = Piece("offense")
    board.board_state[5][6] = Piece("offense")
    board.board_state[6][5] = Piece("offense")

    assert board._run_algorithm_for_encircled_defenders() is False


def test_check_for_2_pieces_of_team_next_to_square():
    # Two matching adjacent pieces return True.
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.board_state[4][4] = Piece("defense")
    board.board_state[6][6] = Piece("defense")

    assert board._check_for_2_pieces_of_team_next_to_square(
        (5, 5), "defense"
    ) is True

    # Fewer than two matching pieces return False.
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.board_state[4][4] = Piece("defense")
    board.board_state[4][5] = Piece("offense")

    assert board._check_for_2_pieces_of_team_next_to_square(
        (5, 5), "defense"
    ) is False

    # Matching pieces near the board edge are counted safely.
    board = Board()
    board.board_state = [[None] * 11 for _ in range(11)]
    board.board_state[9][9] = Piece("defense")
    board.board_state[9][10] = Piece("defense")

    assert board._check_for_2_pieces_of_team_next_to_square(
        (10, 10), "defense"
    ) is True


if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
