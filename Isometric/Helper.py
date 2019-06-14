import pygame

RESOLUTION = (1600, 900)

BLOCK_MATERIALS = dict(
    sand=(60, 60, 0),
    grass=(0, 50, 0),
    dirt=(50, 15, 0),
    rock=(15, 15, 15),
    clay=(60, 60, 40),
    default=(0, 0, 0)
)

pygame.display.init()

DISPLAY_SURFACE = pygame.display.set_mode(RESOLUTION)
