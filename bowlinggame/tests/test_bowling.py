import pytest

from bowlinggame.model.bowling import Game


@pytest.fixture
def game():
    return Game()


def roll_many(game, n, pins):
    for _ in range(n):
        game.roll(pins)


def roll_spare(game):
    game.roll(5)
    game.roll(5)


def roll_strike(game):
    game.roll(10)


def test_game_where_no_pins_were_knocked_down():
    # Arrange (Organizar las variables)
    game = Game()

    # Act (Una acción que quiera probar)
    for _ in range(20):
        game.roll(0)

    # Assert (Verificar si fue un resultado positivo o negativo)
    assert game.score() == 0


def test_all_ones_game():
    # Arrange ( Para no repetir siempre el mismo arrange, vamos a usarfixture que me automatiza lo que estoy repitiendo)
    game = Game()

    for _ in range(20):
        game.roll(1)

    assert game.score() == 20

# Modularizando...


def test_one_spare_game(game):
    """El nombre del parámetro debe ser tal cual el nombre de la funcion creada fixture"""
    roll_spare(game)
    game.roll(6)
    roll_many(game, 17, 0)
    assert game.score() == 22


def test_one_strike_game(game):
    roll_strike(game)
    game.roll(3)
    game.roll(4)
    roll_many(game, 16, 0)
    assert game.score() == 24


def test_perfect_game(game):
    roll_many(game, 12, 10)
    assert 300 == game.score()


def test_game_with_all_spares(game):
    for _ in range(10):
        roll_spare(game)
    game.roll(5)
    assert 150 == game.score()

# IMPORTANTE: investigar sobre exresiones regulares
# Tambien se deben probar que se arrojen correctamente las excepciones
# En el match debería ir una expresion regular


def test_raise_exception_when_frame_rolls_exceed_10_pins(game):
    with pytest.raises(ValueError, match="A frame's rolls cannot exceed 10 pins"):
        game.roll(6)
        game.roll(7)


def test_raise_exception_when_bonus_roll_with_open_tenth_frame(game):
    roll_many(game, 20, 0)
    with pytest.raises(IndexError, match="Can't throw bonus roll with an open tenth frame"):
        game.roll(0)


def test_raise_exception_when_tenth_frame_with_more_than_3_rolls(game):
    roll_many(game, 12, 10)
    with pytest.raises(IndexError, match="Can't add more than three rolls to the tenth frame"):
        game.roll(0)


def test_raise_exception_when_calculate_score_without_game_end(game):
    roll_many(game, 10, 2)
    with pytest.raises(IndexError, match="There are not enough frames to calculate score"):
        game.score()
