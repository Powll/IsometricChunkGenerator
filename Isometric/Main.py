from Block import Blocks
import pygame
from Helper import DISPLAY_SURFACE
from Helper import RESOLUTION
from ImageHelper import PLAYER_TEXTURES
import random


pygame.display.init()

display = DISPLAY_SURFACE

player = PLAYER_TEXTURES['placeholder']

smoothness = 2
# chunk = Blocks(16, 16, 32, smoothness, water_level=16 + random.randint(-6, 0), water=True)
chunk_index = 0

FPS_CLOCK = pygame.time.Clock()
FPS = 60

running = True

offset_x = int(RESOLUTION[0] / 2)
offset_y = int(RESOLUTION[1] / 4)

move_distance = 48

chunks = None

map_width = 4
map_height = 4

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                offset_y += move_distance
            if event.key == pygame.K_a:
                offset_x += move_distance
            if event.key == pygame.K_s:
                offset_y -= move_distance
            if event.key == pygame.K_d:
                offset_x -= move_distance
            if event.key == pygame.K_e:
                pygame.image.save(display, "chunk" + str(chunk_index) + ".png")
                chunk_index += 1

            display.fill((25, 100, 200))

            if chunks:
                for chunks_y in range(0, map_height):

                    chunks_offset_y = chunks_y * 8 * 24

                    chunks_offset_x = (chunks_y % 2) * 8 * 48

                    for chunks_x in range(0, map_width):
                        chunks_offset_x -= chunks_x * 16 * 48

                        print(chunks_offset_x, chunks_offset_y)

                        for x in range(0, chunks[chunks_x][chunks_y].size[0]):

                            for y in range(0, chunks[chunks_x][chunks_y].size[1]):

                                for z in range(0, chunks[chunks_x][chunks_y].size[2]):

                                    if chunks[chunks_x][chunks_y].blocks[x][y][z].type != 'empty':

                                        if x < len(chunks[chunks_x][chunks_y].blocks) - 1 and y < len(chunks[chunks_x][chunks_y].blocks) - 1 and z < len(
                                                chunks[chunks_x][chunks_y].blocks[1]) - 1:

                                            if chunks[chunks_x][chunks_y].blocks[x + 1][y + 1][z + 1].type != 'normal':
                                                display.blit(chunks[chunks_x][chunks_y].blocks[x][y][z].texture,
                                                             (chunks[chunks_x][chunks_y].blocks[x][y][z].screen_position[0] + chunks_offset_x + offset_x,
                                                              chunks[chunks_x][chunks_y].blocks[x][y][z].screen_position[1] + chunks_offset_y + offset_y))

                                        elif chunks[chunks_x][chunks_y].blocks[x][y][z].type != 'empty':

                                            display.blit(chunks[chunks_x][chunks_y].blocks[x][y][z].texture,
                                                         (chunks[chunks_x][chunks_y].blocks[x][y][z].screen_position[0] + chunks_offset_x + offset_x,
                                                          chunks[chunks_x][chunks_y].blocks[x][y][z].screen_position[1] + chunks_offset_y + offset_y))

            if event.key == pygame.K_p:

                chunks = [[Blocks(16, 16, 16, 1.75, water_level=6, water=True) for x in range(0, map_width)] for y in range(0, map_height)]

                for chunks_y in range(0, map_height):

                    chunks_offset_y = chunks_y * 8 * 24

                    chunks_offset_x = (chunks_y % 2) * 8 * 48

                    for chunks_x in range(0, map_width):
                        chunks_offset_x += chunks_x * 16 * 48

                        print(chunks_offset_x, chunks_offset_y)

                        for x in range(0, chunks[chunks_x][chunks_y].size[0]):

                            for y in range(0, chunks[chunks_x][chunks_y].size[1]):

                                for z in range(0, chunks[chunks_x][chunks_y].size[2]):

                                    if chunks[chunks_x][chunks_y].blocks[x][y][z].type != 'empty':

                                        if x < len(chunks[chunks_x][chunks_y].blocks) - 1 and y < len(chunks[chunks_x][chunks_y].blocks) - 1 and z < len(
                                                chunks[chunks_x][chunks_y].blocks[1]) - 1:

                                            if chunks[chunks_x][chunks_y].blocks[x + 1][y + 1][z + 1].type != 'normal':
                                                display.blit(chunks[chunks_x][chunks_y].blocks[x][y][z].texture,
                                                             (chunks[chunks_x][chunks_y].blocks[x][y][z].screen_position[0] + chunks_offset_x + offset_x,
                                                              chunks[chunks_x][chunks_y].blocks[x][y][z].screen_position[1] + chunks_offset_y + offset_y))

                                        elif chunks[chunks_x][chunks_y].blocks[x][y][z].type != 'empty':

                                            display.blit(chunks[chunks_x][chunks_y].blocks[x][y][z].texture,
                                                         (chunks[chunks_x][chunks_y].blocks[x][y][z].screen_position[0] + chunks_offset_x + offset_x,
                                                          chunks[chunks_x][chunks_y].blocks[x][y][z].screen_position[1] + chunks_offset_y + offset_y))


            pygame.display.flip()
            FPS_CLOCK.tick(FPS)
