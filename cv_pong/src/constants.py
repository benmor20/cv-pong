"""
Where constants are held for Pong
"""

# Display constants
WINDOW_SIZE = (800, 600)  # pixels by pixels
WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE
FRAME_RATE = 60  # frames per second


# Court constants
WALL_THICKNESS = 20  # pixels
PADDLE_DIST_FROM_EDGE = 20  # pixels


# Ball constants
BALL_SIZE = 50  # pixels
BALL_INITIAL_SPEED = 100  # pixels in each direction per second
BALL_SPEED_FACTOR = 1.05


# Paddle constants
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20


# Colors
BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)
BALL_COLOR = WALL_COLOR
PADDLE_COLOR = BALL_COLOR
