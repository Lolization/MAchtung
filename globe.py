import math


SERVER = "10.0.0.11"
PORT = 5555

START_SPEED = 0.7
START_WIDTH = 8

GAP_PROB = 0.003

WIDTH = HEIGHT = 500


def rad_to_degree(rads):
    return rads / (180 / math.pi)


def degree_to_rad(degree):
    return degree * (180 / math.pi)
