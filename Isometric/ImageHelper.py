import pygame
from Helper import RESOLUTION

pygame.display.init()
screen = pygame.display.set_mode(RESOLUTION, 0, 32)

BLOCK_TEXTURES = dict(
    normal="Block_Normal.png",
    empty="Block_Empty.png",
    ramp="Block_Ramp.png",
    ramp_alt="Block_Ramp_Alt.png",
    corner="Block_Corner.png",
    corner_inv="Block_Corner_Inv.png",
    water="Water.png"
)

PLAYER_TEXTURES = dict(
    placeholder=pygame.image.load("Player_Placeholder.png").convert_alpha()
)


