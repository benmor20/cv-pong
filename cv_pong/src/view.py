"""
A module defining different views for the Pong game
"""
from abc import ABC, abstractmethod
from .model import PongModel


class PongView(ABC):
    def __init__(self, model: PongModel):
        self._model = model
