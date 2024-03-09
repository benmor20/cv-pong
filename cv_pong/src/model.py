"""
A model the current game state of a game of Pong
"""
from .constants import *
from .utils import add_tuples, scale_tuple, do_rects_intersect


class PongModel:
    """
    A model holding the current state of the game of Pong
    """
    def __init__(self,
                 ball_pos: tuple[int, int] = scale_tuple(WINDOW_SIZE, 0.5),
                 ball_vel: tuple[float, float] = (float(BALL_INITIAL_SPEED),
                                                  -float(BALL_INITIAL_SPEED)),
                 paddle_location: int = WINDOW_HEIGHT // 2,
                 ):
        """
        Initialize a new game of Pong
        """
        # All X/Y positions are defined from the top left of the screen
        # So Y increases down (to match OpenCV)
        self._ball_pos = tuple(float(p) for p in ball_pos)
        self._ball_vel = ball_vel
        self._paddle_location = 0
        self.move_paddle(paddle_location)
        self._points = 0

    @property
    def ball_pos(self) -> tuple[int, int]:
        """
        :return: the x/y position of the ball, where x is pixels from the left
            and y is pixels from the top
        """
        return int(self._ball_pos[0]), int(self._ball_pos[1])

    @property
    def ball_vel(self) -> tuple[float, float]:
        """
        :return: the x/y velocity of the ball
        """
        return self._ball_vel

    @property
    def paddle_location(self) -> int:
        """
        :return: an int, the y-pixel coordinate of the center of the paddle
        """
        return self._paddle_location

    @property
    def points(self) -> int:
        """
        :return: an int, the number of points the player has scored
        """
        return self._points

    def move_paddle(self, coordinate_to_move_paddle: int):
        """
        Move the paddle to the specified coordinate

        If the given position is out of range, will move the paddle to the edge
        of the board in the direction of that range

        :param coordinate_to_move_paddle: an int, the y pixel coordinate to set
            the middle of the paddle to
        """
        min_pos = WALL_THICKNESS + PADDLE_HEIGHT // 2
        max_pos = WINDOW_HEIGHT - min_pos
        self._paddle_location = min(max(coordinate_to_move_paddle, min_pos),
                                    max_pos)

    def update(self):
        """
        Update the state of the game
        """
        # Find next position
        effective_vel = scale_tuple(self.ball_vel, 1.0 / FRAME_RATE)
        self._ball_pos = add_tuples(self.ball_pos, effective_vel)

        # Bounce the ball off top/bottom wall
        top_of_ball = int(self.ball_pos[1]) - BALL_SIZE // 2
        bottom_of_ball = top_of_ball + BALL_SIZE
        if top_of_ball < WALL_THICKNESS \
                or bottom_of_ball > WINDOW_HEIGHT - WALL_THICKNESS:
            self._ball_vel = self.ball_vel[0], -self.ball_vel[1]

        # Bounce the ball off the back wall
        # One point and increase speed
        # TODO speed caps or deal with absurd speeds
        left_of_ball = int(self.ball_pos[0]) - BALL_SIZE // 2
        if left_of_ball < WALL_THICKNESS:
            self._ball_vel = abs(self.ball_vel[0]), self.ball_vel[1]
            self._ball_vel = tuple(
                float(int(val * BALL_SPEED_FACTOR)) for val in self.ball_vel
            )  # Round off but keep type as float
            self._points += 1

        # Bounce the ball off the paddle
        ball_rect = left_of_ball, top_of_ball, BALL_SIZE, BALL_SIZE
        paddle_rect = (
            WINDOW_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH,
            self.paddle_location - PADDLE_HEIGHT // 2,
            PADDLE_WIDTH, PADDLE_HEIGHT
        )
        if do_rects_intersect(ball_rect, paddle_rect):
            self._ball_vel = -abs(self.ball_vel[0]), self.ball_vel[1]

        # Missed - minus one point
        if self.ball_pos[0] > WINDOW_WIDTH:
            self._points -= 1
            self._ball_pos = scale_tuple(WINDOW_SIZE, 0.5)
            # Don't need to change velocity - its already moving right
