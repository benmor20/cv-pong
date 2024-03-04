"""
A module defining different views for the Pong game
"""
from abc import ABC, abstractmethod
import pygame
from .constants import *
from .model import PongModel
from .utils import *


class PongView(ABC):
    """
    An abstract class representing a viewer for Pong
    """
    def __init__(self, model: PongModel):
        """
        Sets up a new PongView

        :param model: the PongModel representing the game this viewer draws
        """
        self._model = model

    @abstractmethod
    def draw(self):
        """
        Draw the current state of the game
        """
        pass


class PygameView(PongView):
    """
    A viewer displayed using pygame
    """
    def __init__(self, model: PongModel, screen: pygame.Surface):
        """
        Sets up a new PygameView

        :param model: the PongModel representing the game this viewer draws
        :param screen: the pygame Surface to draw the game on
        """
        super().__init__(model)
        self._screen = screen

    def draw(self):
        # Draw court
        self._screen.fill(WALL_COLOR)
        court_rect = pygame.Rect(
            WALL_THICKNESS, WALL_THICKNESS,
            WINDOW_WIDTH - WALL_THICKNESS,
            WINDOW_HEIGHT - WALL_THICKNESS * 2
        )
        self._screen.fill(BACKGROUND_COLOR, court_rect)

        # Draw ball
        top_left_ball = add_tuples(
            self._model.ball_pos,
            scale_tuple((BALL_SIZE, BALL_SIZE), -0.5)
        )
        ball_rect = pygame.Rect(int(top_left_ball[0]), int(top_left_ball[1]),
                                BALL_SIZE, BALL_SIZE)
        self._screen.fill(BALL_COLOR, ball_rect)

        # Draw paddle
        paddle_rect = pygame.Rect(
            WINDOW_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH,
            int(self._model.paddle_location) - PADDLE_HEIGHT // 2,
            PADDLE_WIDTH, PADDLE_HEIGHT
        )
        self._screen.fill(PADDLE_COLOR, paddle_rect)

        # Draw score
        score = SCORE_FONT.render(str(self._model.points), True, SCORE_COLOR)
        self._screen.blit(score, score.get_rect(midtop=SCORE_TOP_CENTER))

        pygame.display.flip()
