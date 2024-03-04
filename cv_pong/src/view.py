"""
A module defining different views for the Pong game
"""
from __future__ import annotations

from abc import ABC, abstractmethod
import pygame
from .constants import *
from .controller import CVController
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
    def __init__(self,
                 model: PongModel,
                 screen: pygame.Surface,
                 controller: CVController | None = None):
        """
        Sets up a new PygameView

        :param model: the PongModel representing the game this viewer draws
        :param screen: the pygame Surface to draw the game on
        :param controller: the CVController which holds the live camera feed
            to display as a background, or None to not display camera feed
        """
        super().__init__(model)
        self._screen = screen
        self._cv_controller = controller

    def draw(self):
        # Draw camera feed
        draw_cam_feed = self._cv_controller is not None
        if draw_cam_feed:
            frame = self._cv_controller.camera_frame
            image = pygame.pixelcopy.make_surface(frame)
            self._screen.blit(image, (0, 0))

        # Draw court
        if draw_cam_feed:
            court = pygame.Surface(
                (WINDOW_WIDTH - WALL_THICKNESS,
                 WINDOW_HEIGHT - 2 * WALL_THICKNESS),
                pygame.SRCALPHA
            )
            court.fill(BACKGROUND_COLOR_TRANSPARENT)
            self._screen.blit(court, (WALL_THICKNESS, WALL_THICKNESS))
        else:
            self._screen.fill(BACKGROUND_COLOR)
        top_wall = pygame.Rect(0, 0, WINDOW_WIDTH, WALL_THICKNESS)
        left_wall = pygame.Rect(0, 0, WALL_THICKNESS, WINDOW_HEIGHT)
        bottom_wall = pygame.Rect(0, WINDOW_HEIGHT - WALL_THICKNESS,
                                  WINDOW_WIDTH, WALL_THICKNESS)
        self._screen.fill(WALL_COLOR, top_wall)
        self._screen.fill(WALL_COLOR, left_wall)
        self._screen.fill(WALL_COLOR, bottom_wall)

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
