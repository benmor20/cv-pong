"""
A model the current game state of a game of Pong
"""
from .constants import *
from .utils import add_tuples, scale_tuple


class PongModel:
    """
    A model holding the current state of the game of Pong

    Attributes:
        paddle_location: an int, the Y position of the center of the paddle
    """
    def __init__(self):
        """
        Initialize a new game of Pong
        """
        # All X/Y positions are defined from the top left of the screen
        # So Y increases down (to match OpenCV)
        self._ball_pos = scale_tuple(WINDOW_SIZE, 0.5)
        self._ball_vel = (BALL_INITIAL_SPEED, -BALL_INITIAL_SPEED)
        self.paddle_location = WINDOW_HEIGHT // 2
        self._points = 0

    @property
    def ball_pos(self) -> tuple[int, int]:
        """
        :return: the position of the ball as a complex number, where the real
            part gives the distance in pixels from the left of the screen, and
            the complex part gives the distance in pixels from the top
        """
        return self._ball_pos

    @property
    def ball_vel(self) -> tuple[int, int]:
        """
        :return: the velocity of the ball as a complex number, represented in
            pixels per second
        """
        return self._ball_vel

    @property
    def points(self) -> int:
        """
        :return: an int, the number of points the player has scored
        """
        return self._points

    def update(self):
        """
        Update the state of the game
        """
        # Find next position
        effective_vel = scale_tuple(self.ball_vel, 1.0 / FRAME_RATE)
        self._ball_pos = self.ball_pos + effective_vel

        # Bounce the ball off top/bottom wall
        top_of_ball = self.ball_pos[1] - BALL_SIZE // 2
        bottom_of_ball = top_of_ball + BALL_SIZE
        if top_of_ball < WALL_THICKNESS \
                or bottom_of_ball > WINDOW_HEIGHT - WALL_THICKNESS:
            self._ball_vel = self.ball_vel[0], -self.ball_vel[1]

        # Bounce the ball off the back wall
        # One point and increase speed
        # TODO speed caps or deal with absurd speeds
        left_of_ball = self.ball_pos[0] - BALL_SIZE // 2
        if left_of_ball < WALL_THICKNESS:
            self._ball_vel = -self.ball_vel[0], self.ball_vel[1]
            self._ball_vel = scale_tuple(self.ball_vel, BALL_SPEED_FACTOR)
            self._points += 1

        # Missed - minus one point
        if self.ball_pos[0] > WINDOW_WIDTH:
            self._points -= 1
            self._ball_pos = scale_tuple(WINDOW_SIZE, 0.5)
            # Dont need to change velocity - its already moving right
