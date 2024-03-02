"""
A module defining various controllers for one player in Pong
"""
from abc import ABC, abstractmethod
from .model import PongModel


class PongController(ABC):
    def __init__(self, model: PongModel):
        self._model = model
