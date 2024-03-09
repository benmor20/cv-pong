"""
Tests for PongModel
"""
import pytest
from ..src.model import PongModel
from ..src.constants import *


CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2
HALF_BALL = BALL_SIZE // 2


def pix_per_sec(*pix_per_frame: float | int) -> tuple[float | int, float | int]:
    """
    Convert pixels per seconds to pixels per frame

    :param pix_per_frame: the x and y speed in pixels per frame
    :return: a tuple of two floats or int (same type as input), the x and y
        speed in pixels per second
    """
    return pix_per_frame[0] * FRAME_RATE, pix_per_frame[1] * FRAME_RATE


# Each element is a tuple consisting of:
# - the initial ball position (two-int tuple)
# - the initial ball velocity (two-int tuple)
# - the initial paddle location (int)
# - the next ball position (two-int tuple)
# - the next ball velocity (two-int tuple)
BALL_MOTION_TESTS = [
    # Ball moves in empty space
    ((CENTER_X, CENTER_Y), pix_per_sec(1, 1), 0,
     (CENTER_X + 1, CENTER_Y + 1), pix_per_sec(1, 1)),
    ((CENTER_X, CENTER_Y), pix_per_sec(1, -2), 0,
     (CENTER_X + 1, CENTER_Y - 2), pix_per_sec(1, -2)),
    ((CENTER_X, CENTER_Y), pix_per_sec(-1, 1), 0,
     (CENTER_X - 1, CENTER_Y + 1), pix_per_sec(-1, 1)),
    ((CENTER_X // 2, CENTER_Y), pix_per_sec(1, 1), 0,
     (CENTER_X // 2 + 1, CENTER_Y + 1), pix_per_sec(1, 1)),
    ((CENTER_X, CENTER_Y // 2), pix_per_sec(1, -2), 0,
     (CENTER_X + 1, CENTER_Y // 2 - 2), pix_per_sec(1, -2)),
    ((CENTER_X // 2, CENTER_Y // 2), pix_per_sec(-1, 1), 0,
     (CENTER_X // 2 - 1, CENTER_Y // 2 + 1), pix_per_sec(-1, 1)),
    # Ball hit top/bottom wall
    ((CENTER_X, WALL_THICKNESS + HALF_BALL + 2), pix_per_sec(1, -3), 0,
     (CENTER_X + 1, WALL_THICKNESS + HALF_BALL - 1), pix_per_sec(1, 3)),
    ((CENTER_X // 2, WINDOW_HEIGHT - WALL_THICKNESS - HALF_BALL - 2),
     pix_per_sec(-2, 4), 0,
     (CENTER_X // 2 - 2, WINDOW_HEIGHT - WALL_THICKNESS - HALF_BALL + 2),
     pix_per_sec(-2, -4)),
    # Ball hit left wall
    ((WALL_THICKNESS + HALF_BALL + 1, CENTER_Y), pix_per_sec(-4, -3), 0,
     (WALL_THICKNESS + HALF_BALL - 3, CENTER_Y - 3),
     pix_per_sec(4 * BALL_SPEED_FACTOR, -3 * BALL_SPEED_FACTOR)),
    # Ball hit paddle
    ((WINDOW_WIDTH - PADDLE_DIST_FROM_EDGE, CENTER_Y), pix_per_sec(1, 1),
     CENTER_Y, (WINDOW_WIDTH - PADDLE_DIST_FROM_EDGE + 1, CENTER_Y + 1),
     pix_per_sec(-1, 1)),
    # Ball moves outside screen
    ((WINDOW_WIDTH + HALF_BALL + 10, CENTER_Y), pix_per_sec(1, 1), 0,
     (CENTER_X, CENTER_Y), pix_per_sec(1, 1))
]


# Each element is a tuple containing:
# - an int, the place to ask the model to initialize the paddle
# - an int, the place the model should initialize the paddle
PADDLE_INIT_CASES = [
    # Middle of screen
    (CENTER_Y, CENTER_Y),
    (CENTER_Y // 2, CENTER_Y // 2),
    # Near top edge
    (WALL_THICKNESS + PADDLE_HEIGHT // 2, WALL_THICKNESS + PADDLE_HEIGHT // 2),
    # Near bottom edge
    (WINDOW_HEIGHT - WALL_THICKNESS - PADDLE_HEIGHT // 2,
     WINDOW_HEIGHT - WALL_THICKNESS - PADDLE_HEIGHT // 2),
    # Above top edge
    (1, WALL_THICKNESS + PADDLE_HEIGHT // 2),
    (0, WALL_THICKNESS + PADDLE_HEIGHT // 2),
    (-10, WALL_THICKNESS + PADDLE_HEIGHT // 2),
    # Below bottom edge
    (WINDOW_HEIGHT - 1, WINDOW_HEIGHT - WALL_THICKNESS - PADDLE_HEIGHT // 2),
    (WINDOW_HEIGHT, WINDOW_HEIGHT - WALL_THICKNESS - PADDLE_HEIGHT // 2),
    (WINDOW_HEIGHT + 10, WINDOW_HEIGHT - WALL_THICKNESS - PADDLE_HEIGHT // 2)
]
PADDLE_MOTION_TESTS = PADDLE_INIT_CASES


@pytest.mark.parametrize("init_pos, init_vel, init_paddle, next_pos, next_vel",
                         BALL_MOTION_TESTS)
def test_motion_of_ball(init_pos: tuple[int, int], init_vel: tuple[int, int],
                        init_paddle: int, next_pos: tuple[int, int],
                        next_vel: tuple[int, int]):
    """
    Test that the ball moves in the correct manner

    :param init_pos: a tuple of two ints, the starting position of the ball
    :param init_vel: a tuple of two ints, the starting velocity of the ball
        in pixels per second
    :param init_paddle: an int, the initial y-position of the center of the
        paddle
    :param next_pos: a tuple of two ints, the next position of the ball
    :param next_vel: a tuple of two ints, the next velocity of the ball
    """
    model = PongModel(init_pos, init_vel, init_paddle)
    model.update()
    assert model.ball_pos == next_pos
    assert pytest.approx(model.ball_vel[0]) == next_vel[0]
    assert pytest.approx(model.ball_vel[1]) == next_vel[1]


@pytest.mark.parametrize("init_pos, actual_pos", PADDLE_INIT_CASES)
def test_paddle_initialization(init_pos: int, actual_pos: int):
    """
    Test that the paddle initialization constrains the paddle to the screen

    :param init_pos: an int, the position of the paddle to attempt to
        initialize to
    :param actual_pos: an int, the position the paddle should initialize to
    """
    model = PongModel(paddle_location=init_pos)
    assert model.paddle_location == actual_pos


@pytest.mark.parametrize("move_pos, actual_pos", PADDLE_MOTION_TESTS)
def test_paddle_motion(move_pos: int, actual_pos: int):
    """
    Test that the moving the paddle constrains it to the screen

    :param move_pos: an int, the position of the paddle to attempt to move to
    :param actual_pos: an int, the position the paddle should move to
    """
    model = PongModel()
    model.move_paddle(move_pos)
    assert model.paddle_location == actual_pos


def test_point_increase():
    """
    Test that the score increases when the ball hits the left wall
    """
    model = PongModel(
        ball_pos=(WALL_THICKNESS + HALF_BALL + 1, CENTER_Y),
        ball_vel=pix_per_sec(-4, -3)
    )
    assert model.points == 0
    model.update()
    assert model.points == 1


def test_point_decrease():
    """
    Test the score decreases when the ball passes the right edge
    """
    model = PongModel(
        ball_pos=(WINDOW_WIDTH + HALF_BALL + 10, CENTER_Y)
    )
    assert model.points == 0
    model.update()
    assert model.points == -1
