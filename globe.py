import math

# Connections
SERVER = "10.0.0.11"
PORT = 5000

# Snake initializations
START_SPEED = 0.8
START_WIDTH = 8
GAP_PROB = 0.003

# Pygame Graphics
WIDTH = HEIGHT = 500
BACKGROUND_COLOR = (107, 15, 93)  # Deep Purple
INVERT = [179, 235, 187]
FONT_SIZE = 64


def degree_to_rad(rads):
    return rads / (180 / math.pi)


def rad_to_degree(degree):
    return degree * (180 / math.pi)
