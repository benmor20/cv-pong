"""
A module defining various controllers for one player in Pong
"""
from abc import ABC, abstractmethod
import cv2
import mediapipe as mp
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


class CameraClosedException(Exception):
    pass


class CVController(PongController):
    """
    A controller that moves by detecting
    """
    def __init__(self, model: PongModel):
        """
        Set up a new CVController

        :param model: the PongModel representing the game this controller
            operates in
        """
        super().__init__(model)
        self._video_capture = None
        self._hand_processor = None

    def initialize(self, *cam_args, **cam_kwargs):
        """
        Initialize this CVController

        Starts the video capture process and sets up mediapipe's hand tracker
        """
        if len(cam_args) == 0 and len(cam_kwargs) == 0:
            self._video_capture = cv2.VideoCapture(0)
        else:
            self._video_capture = cv2.VideoCapture(*cam_args, **cam_kwargs)
        self._hand_processor = mp.solutions.hands.Hands()

    def move(self):
        if not self._video_capture.isOpened():
            raise CameraClosedException('Camera has been closed')
        ret, frame = self._video_capture.read()
        if not ret:
            raise CameraClosedException('Could not read from camera')
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hands = self._hand_processor.process(rgb_frame)
        if hands.multi_hand_landmarks:
            landmarks = hands.multi_hand_landmarks[0].landmark
            # estimated middle of hand is between base of palm and base of
            # middle finger
            mid_hand = (landmarks[0].y + landmarks[9].y) / 2
            paddle_position = int(mid_hand * WINDOW_HEIGHT)
            self._model.move_paddle(paddle_position)
