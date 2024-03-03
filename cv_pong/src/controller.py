"""
A module defining various controllers for one player in Pong
"""
from abc import ABC, abstractmethod
import pygame
from pygame import locals
from .constants import *
from .model import PongModel


class PongController(ABC):
    """
    An abstract class representing a controller for Pong
    """
    def __init__(self, model: PongModel):
        """
        Set up a new PongController

        :param model: the PongModel representing the game this controller
            operates in
        """
        self._model = model

    @abstractmethod
    def move(self):
        """
        Control the player's paddle
        """
        pass


class KeyboardController(PongController):
    """
    A controller that moves using the keyboard
    """
    def __init__(self, model: PongModel):
        """
        Set up a new KeyboardController

        :param model: the PongModel representing the game this controller
            operates in
        """
        super().__init__(model)
        self._up_key_pressed = False
        self._down_key_pressed = False

    def _update_key_presses(self):
        """
        Updates the flags to tell whether a key is held down
        """
        # Detect new key presses
        for event in pygame.event.get(locals.KEYDOWN):
            if event.key == locals.K_UP:
                self._up_key_pressed = True
            if event.key == locals.K_DOWN:
                self._down_key_pressed = True

        # Detect key releases
        for event in pygame.event.get(locals.KEYUP):
            if event.key == locals.K_UP:
                self._up_key_pressed = False
            if event.key == locals.K_DOWN:
                self._down_key_pressed = False

    def move(self):
        self._update_key_presses()

        if self._up_key_pressed and not self._down_key_pressed:
            self._model.move_paddle(
                self._model.paddle_location - KEYBOARD_PADDLE_SPEED_PER_FRAME
            )
        elif self._down_key_pressed and not self._up_key_pressed:
            self._model.move_paddle(
                self._model.paddle_location + KEYBOARD_PADDLE_SPEED_PER_FRAME
            )
