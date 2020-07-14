import math

# Connections
SERVER = "10.0.0.28"
PORT = 5555

# Snake initializations
START_SPEED = 1
START_WIDTH = 8
GAP_PROB = 0.003

# Pygame Graphics
WIDTH = HEIGHT = 500
BACKGROUND_COLOR = (107, 15, 93)  # Deep Purple
INVERT = [179, 235, 187]
FONT_SIZE = 64


def rad_to_degree(rads):
    return rads / (180 / math.pi)


def degree_to_rad(degree):
    return degree * (180 / math.pi)