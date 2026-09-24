import pytest
from hnefatafl import Board, Piece


def test_piece_init():
    offense = Piece("offense", "standard")
    assert offense.is_captured == False
    assert offense.type == "standard"
    assert offense.team == "offense"
    assert offense.character == "A"

    defense = Piece("defense")
    assert defense.is_captured == False
    assert defense.type == "standard"
    assert defense.team == "defense"
    assert defense.character == "D"
    king = Piece("defense", type="king")
    assert king.is_captured == False
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

def test_translate_text_into_coorinate():
    board = Board()
    assert board.translate_text_into_coorinate("A4") == (3, 0)
    assert board.translate_text_into_coorinate("K11") == (10, 10)
    assert board.translate_text_into_coorinate("h5") == (4, 7)

    with pytest.raises(ValueError):
        board.translate_text_into_coorinate ("L10")
    with pytest.raises(ValueError):
        board.translate_text_into_coorinate("A13")
    with pytest.raises(ValueError):
        board.translate_text_into_coorinate("A")
        board.translate_text_into_coorinate("AB")
        board.translate_text_into_coorinate("A1C")

pytest.main(["-v", "--tb=line", "-rN", __file__])
