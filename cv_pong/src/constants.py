"""
Where constants are held for Pong
"""

# Display constants
WINDOW_SIZE = (800, 600)  # pixels by pixels
WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE
FRAME_RATE = 60  # frames per second


# Court constants
WALL_THICKNESS = 20  # pixels
PADDLE_DIST_FROM_EDGE = 40  # pixels. distance to right edge of paddle


# Ball constants
BALL_SIZE = 50  # pixels
BALL_INITIAL_SPEED = 150  # pixels in each direction per second
BALL_SPEED_FACTOR = 1.2


# Paddle constants
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
KEYBOARD_PADDLE_SPEED = 200
KEYBOARD_PADDLE_SPEED_PER_FRAME = KEYBOARD_PADDLE_SPEED // FRAME_RATE


# Score constants
SCORE_TOP_CENTER = (WINDOW_WIDTH // 2, WALL_THICKNESS + 10)


# Colors
BACKGROUND_COLOR = (0, 0, 0)
BACKGROUND_COLOR_TRANSPARENT = (*BACKGROUND_COLOR, 192)
WALL_COLOR = (255, 255, 255)
SCORE_COLOR = WALL_COLOR
BALL_COLOR = WALL_COLOR
PADDLE_COLOR = BALL_COLOR


# Fonts
import pygame.font
pygame.font.init()

SCORE_FONT = pygame.font.SysFont('monospace', 48, True)
