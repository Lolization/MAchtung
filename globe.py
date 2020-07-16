import math

# Connections
TERMI_NONLOCAL = "79.177.97.115"
DORI_LOCAL = "10.100.102.209"
SERVER = DORI_LOCAL
PORT = 5555

# Snake initializations
START_SPEED = 0.8
START_WIDTH = 8
GAP_PROB = 0.003

# Pygame Graphics
WIDTH = HEIGHT = 500
BACKGROUND_COLOR = (107, 15, 93)  # Deep Purple
INVERT = [179, 235, 187]
FONT_SIZE = 64


# Degrees conversions
def degree_to_rad(rads: float) -> float:
    return rads / (180 / math.pi)


def rad_to_degree(degree: float) -> float:
    return degree * (180 / math.pi)
