import ImageHelper
import scipy.ndimage
import noise
import random
import pygame
from Helper import BLOCK_MATERIALS
import os

class Block:

    BLOCK_MATERIAL_TEXTURES = dict()
    created_material_textures = False

    def __init__(self, x, y, z, block_type='empty', block_material='default'):
        self.texture = pygame.image.load(ImageHelper.BLOCK_TEXTURES[block_type])
        self.type = block_type
        self.material = block_material
        self.rect = self.texture.get_rect()
        self.position = (x, y, z)
        self.texture_width = self.texture.get_width()
        self.texture_height = self.texture.get_height()
        if Block.created_material_textures is False:
            self.set_materials()
            Block.created_material_textures = True
        del self.texture
        self.texture = Block.BLOCK_MATERIAL_TEXTURES[block_material][block_type]
        self.screen_position = self.calculate_positions(x, y, z)

    def set_materials(self):
        for material in BLOCK_MATERIALS:
            Block.BLOCK_MATERIAL_TEXTURES[material] = dict()
            for texture in ImageHelper.BLOCK_TEXTURES:
                if not os.path.exists('./Resources/Visual/Blocks/' + material + '_' + texture + '.png'):
                    Block.BLOCK_MATERIAL_TEXTURES[material][texture] = pygame.image.load(ImageHelper.BLOCK_TEXTURES[texture])
                    for x in range(0, self.texture_width):
                        for y in range(0, self.texture_height):
                            old_pixel = Block.BLOCK_MATERIAL_TEXTURES[material][texture].get_at((x, y))
                            new_pixel = (max(0, min(255, old_pixel.r + BLOCK_MATERIALS[material][0])),
                                         max(0, min(255, old_pixel.g + BLOCK_MATERIALS[material][1])),
                                         max(0, min(255, old_pixel.b + BLOCK_MATERIALS[material][2])),
                                         old_pixel.a)
                            Block.BLOCK_MATERIAL_TEXTURES[material][texture].set_at((x, y), new_pixel)

                    pygame.image.save(Block.BLOCK_MATERIAL_TEXTURES[material][texture], './Resources/Visual/Blocks/' + material + '_' + texture + '.png')
                else:
                    print('./Resources/Visual/Blocks/' + material + '_' + texture + '.png' + ' already exists')
                    Block.BLOCK_MATERIAL_TEXTURES[material][texture] = pygame.image.load(
                        './Resources/Visual/Blocks/' + material + '_' + texture + '.png')

    def calculate_positions(self, x, y, z):
        screen_x = int(x * self.texture_width / 2)
        screen_y = int(x * self.texture_height / 4)

        screen_x -= int(y * self.texture_width / 2)
        screen_y += int(y * self.texture_height / 4)

        screen_y -= int(z * (self.texture_height / 2))

        return screen_x - int(self.texture_width / 2), screen_y - int(self.texture_height / 2)


class Blocks:
    def __init__(self, x_length, y_length, z_length, smooth_scale=0.9, water_level=14, water=False):
        self.size = (x_length, y_length, z_length)

        self.blocks_types = Blocks.generate_3d_array(self.size, smooth_scale, water_level, water)

        self.blocks_materials = Blocks.generate_materials(self.size, self.blocks_types)

        self.blocks = [[[Block(x, y, z, self.blocks_types[x][y][z], self.blocks_materials[x][y][z])
                         for z in range(0, z_length)]
                        for y in range(0, y_length)]
                       for x in range(0, x_length)]

        print('Finished creation of blocks')

        # recommended approach: generate 3d array of block types then use said
        # array to generate the block, effectively copying it

    @staticmethod
    def generate_materials(size, types):
        materials = [[['default' for z in range(0, size[2])] for y in range(0, size[1])] for x in range(0, size[0])]
        for z in range(0, size[2]):
            for y in range(0, size[1]):
                for x in range(0, size[0]):
                    if types[x][y][z] != 'water' and types[x][y][z] != 'empty' and materials[x][y][z] == 'default':
                        roll = random.random()
                        if z < size[2] - 1 and types[x][y][z + 1] != 'empty':
                            if z < (int(size[2] / 4)):
                                materials[x][y][z] = 'rock'
                            else:
                                materials[x][y][z] = 'dirt'
                        else:
                            if types[x][y][z] != 'empty':
                                if roll < 0.975:
                                    materials[x][y][z] = 'grass'
                                else:
                                    materials[x][y][z] = random.choice(('rock', 'clay'))
                        if (z < size[2] - 1 and types[x][y][z + 1] == 'water')\
                                or (x < size[0] - 1 and types[x + 1][y][z] == 'water') \
                                or (y < size[1] - 1 and types[x][y + 1][z] == 'water') \
                                or (x > 1 and types[x - 1][y][z] == 'water') \
                                or (y > 1 and types[x][y - 1][z] == 'water'):
                            if roll < .85:
                                materials[x][y][z] = 'sand'
                            else:
                                materials[x][y][z] = 'clay'

        return materials


    @staticmethod
    def generate_3d_array(size, smooth_scale, water_level=14, water=False):
        types = [[['normal' if z == 0 else 'empty' for z in range(0, size[2])] for y in range(0, size[1])] for x in range(0, size[0])]
        noise_matrix = Blocks.generate_noise(size)
        noise_matrix = Blocks.smooth_noise(noise_matrix, smooth_scale)
        if size[2] > 1:
            for z in range(1, size[2]):
                for x in range(0, size[0]):
                    for y in range(0, size[1]):
                        if z < noise_matrix[x][y]:
                            if types[x][y][z - 1] == 'normal':
                                types[x][y][z] = 'normal'

        if size[2] > 1:
            for z in range(1, size[2]):
                for x in range(0, size[0]):
                    for y in range(0, size[1]):
                        if types[x][y][z - 1] == 'normal' and types[x][y][z] == 'empty':
                            if y > 1 and types[x][y - 1][z] == 'normal':
                                types[x][y][z] = 'ramp'
                            elif x > 1 and types[x - 1][y][z] == 'normal':
                                types[x][y][z] = 'ramp_alt'
                            elif x > 1 and y > 1 and types[x][y - 1][z] == 'ramp_alt' and types[x - 1][y][z] == 'ramp':
                                types[x][y][z] = 'corner'
                        if x < size[0] - 1 and y < size[1] - 1 and types[x][y + 1][z] == 'ramp_alt' and types[x + 1][y][z] == 'ramp':
                            types[x][y][z] = 'corner_inv'

        if size[2] > 1:
            for z in range(1, size[2]):
                for x in range(0, size[0]):
                    for y in range(0, size[1]):
                        if x < size[0] - 1 and y < size[1] - 1 and (types[x][y + 1][z] == 'ramp_alt' or types[x][y + 1][z] == 'corner') and (types[x + 1][y][z] == 'ramp' or types[x + 1][y][z] == 'corner'):
                                if types[x - 1][y][z] == 'normal' and types[x][y - 1][z] == 'normal':
                                    types[x][y][z] = 'corner_inv'

        if water:
            types = Blocks.add_water(types, water_level, size)
        return types

    @staticmethod
    def add_water(types, water_level, size):
        if size[2] > 1:
            for z in range(1, water_level):
                for x in range(0, size[0]):
                    for y in range(0, size[1]):
                        if types[x][y][z] != 'normal':
                            types[x][y][z] = 'water'
        return types

    @staticmethod
    def generate_noise(size):
        noise_matrix = [[0 for y in range(0, size[1])] for x in range(0, size[0])]
        for y in range(0, size[1]):
            for x in range(0, size[0]):
                noise_matrix[x][y] = int(size[2] / 2 + noise.snoise2(x, y, octaves=6, lacunarity=1.5, base=random.random()) * size[2] / 2)
        return noise_matrix

    @staticmethod
    def smooth_noise(noise_matrix, scale):
        return scipy.ndimage.filters.gaussian_filter(noise_matrix, scale)


