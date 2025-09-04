import pygame
import sys
from pygame.math import Vector2 as vec2
from numpy import sin, cos, radians
import random


WIDTH = 900
HEIGHT = 600

RES_SCALE = 3

RES_WIDTH = WIDTH // RES_SCALE
RES_HEIGHT = HEIGHT // RES_SCALE

TILE = 40 // RES_SCALE
FISH_COLOR = pygame.Color("aqua")
FISH_SPEED = 0.8
FISH_ACC = 0.0006

BIG_FISH_SPEED = 0.2
BIG_FISH_ACC = 0.0003

HOOK_SPEED = 0.3

BUG_FREQ = 0.1

LIGHT_BLUE = (0, 191, 255)
BLUE = (70, 130, 180)
DARK_BLUE = (0, 0, 139)

SEA_DELTA_HEIGHT = 5
SEA_ALPHA = 128
SEA_WAVE_MAGNITUDE = 10
SEA_WAVELENGTH = 120

MOSS_DELTA = 10

PLANKTON_COLOR = pygame.Color("darkmagenta")
BIG_FISH_COLOR = "darkorange4"

ENERGY_BAR_WIDTH = 50
ENERGY_BAR_HEIGHT = 5
ENERGY_BAR_POS = vec2(RES_WIDTH - ENERGY_BAR_WIDTH, 0)