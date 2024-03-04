"""
Main run script for Pong
"""
import pygame
from pygame import locals
from src.constants import *
from src.model import PongModel
from src.view import PygameView
from src.controller import CVController


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.set_alpha(255, pygame.SRCALPHA)

    model = PongModel()
    controller = CVController(model)
    view = PygameView(model, screen, controller)
    controller.initialize()

    clock = pygame.time.Clock()
    exited = False
    while not exited:
        for _ in pygame.event.get(locals.QUIT):
            exited = True

        controller.move()
        model.update()
        view.draw()

        clock.tick(FRAME_RATE)


if __name__ == '__main__':
    main()
