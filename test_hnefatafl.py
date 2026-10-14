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

    #Make sure check_for_capture was called
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][3] = Piece("offense")
    board.board_state[5][4] = Piece("defense")
    board.board_state[5][8] = Piece("offense")

    board.move_piece((5, 8), (5, 5))
    assert board.board_state[5][5].team == "offense"
    assert board.board_state[5][4] is None


def test_check_for_capture_corners():
    #Corner Captures
    board = Board()

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[0][1] = Piece("defense")
    board.board_state[0][2] = Piece("offense")
    board.check_for_capture((0, 2))
    assert board.board_state[0][1] is None
    assert board.board_state[0][2].team == "offense"

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[0][9] = Piece("offense")
    board.board_state[0][8] = Piece("defense")
    board.check_for_capture((0, 8))
    assert board.board_state[0][9] is None


    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[10][1] = Piece("defense")
    board.board_state[10][2] = Piece("offense")
    board.check_for_capture((10, 2))
    assert board.board_state[10][1] is None
    
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[10][9] = Piece("offense")
    board.board_state[10][8] = Piece("defense")
    board.check_for_capture((10, 8))
    assert board.board_state[10][9] is None

def test_for_capture_edges():
    # Board Edges & Boundary Safety (Indices 0, 10, 1, and 9)
    board = Board()

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[4][0] = Piece("defense")
    board.board_state[5][0] = Piece("offense")
    board.board_state[6][0] = Piece("defense")
    board.check_for_capture((6, 0))
    assert board.board_state[5][0] is None

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[0][4] = Piece("defense")
    board.board_state[0][5] = Piece("offense")
    board.board_state[0][6] = Piece("defense")
    board.check_for_capture((0, 6))
    assert board.board_state[0][5] is None
    
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][0] = Piece("defense")
    board.board_state[5][10] = Piece("offense")
    board.board_state[5][1] = Piece("offense")
    board.check_for_capture((5, 1))
    assert board.board_state[5][0].team == "defense"
    

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][10] = Piece("defense")
    board.board_state[5][9] = Piece("offense")
    board.check_for_capture((5, 9))
    assert board.board_state[5][10].team == "defense"

def test_for_capture_throne():
    #Throne Hostility
    board = Board()    

    #empty throne
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[5][6] = Piece("offense")
    board.board_state[5][7] = Piece("defense")
    board.check_for_capture((5, 7))
    assert board.board_state[5][6] is None

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][5] = Piece("defense", type="king")
    board.board_state[5][6] = Piece("defense")
    board.board_state[5][7] = Piece("offense")
    board.check_for_capture((5, 7))
    assert board.board_state[5][6].team == "defense"

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[5][5] = Piece("defense", type="king")
    board.board_state[5][6] = Piece("offense")
    board.board_state[5][7] = Piece("defense")
    board.check_for_capture((5, 7))
    assert board.board_state[5][6] is None

def test_check_for_capture_special():
    #King not captured by 2 pieces
    board = Board()

    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[3][2] = Piece("offense")
    board.board_state[3][3] = Piece("defense", type="king")
    board.board_state[3][4] = Piece("offense")
    board.check_for_capture((3, 4))
    assert board.board_state[3][3].type == "king"

    #Multi-Capture
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[5][7] = Piece("offense")
    board.board_state[6][7] = Piece("defense")
    board.board_state[7][7] = Piece("offense")
    board.board_state[7][8] = Piece("defense")
    board.board_state[7][9] = Piece("offense")
    board.check_for_capture((7, 7))
    assert board.board_state[6][7] is None
    assert board.board_state[7][8] is None

    #Isn't captured when moving between hostile pieces
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "offense"
    board.board_state[7][2] = Piece("defense")
    board.board_state[7][3] = Piece("offense")
    board.board_state[7][4] = Piece("defense")
    board.check_for_capture((7, 3))
    assert board.board_state[7][3].team == "offense"

    #Can't capture friendly pieces
    board.board_state = [[None] * 11 for _ in range(11)]
    board.turn = "defense"
    board.board_state[7][2] = Piece("defense")
    board.board_state[7][3] = Piece("defense")
    board.board_state[7][4] = Piece("defense")
    board.check_for_capture((7, 2))
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
    board.board_state[-1][5] = Piece("offense")
    board.capture_king((0, 5))
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
    board.turn = "offense"
    board.board_state[10][10] = Piece("defense", type = "king")
    board._check_for_king_in_corner()
    assert board.game_over == False
    assert board.victor == ""



pytest.main(["-v", "--tb=line", "-rN", __file__])