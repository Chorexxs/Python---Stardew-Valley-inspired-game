import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS["soil"]

class SoilLayer:
    def __init__(self, all_sprites):
        # Sprites groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # Graphics
        self.soil_surf = pygame.image.load("graphics/soil/o.png")
        self.soil_surfs = import_folder_dict("graphics/soil")
        self.create_soil_grid()
        self.create_hit_rects()
    
    def create_soil_grid(self):
        ground = pygame.image.load("graphics/world/ground.png")
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame("data/map.tmx").get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append("F")
        
    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "F" in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)
    
    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                if "F" in self.grid[y][x]:
                    self.grid[y][x].append("X")
                    self.create_soil_tiles()
    
    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "X" in cell:

                    top = "X" in self.grid[index_row - 1][index_col]
                    bottom = "X" in self.grid[index_row + 1][index_col]
                    right = "X" in row[index_col + 1]
                    left = "X" in row[index_col - 1]
                    tile_type = "o"

                    if all((top,right,bottom,left)):
                        tile_type = "x"
                    
                    if left and not any((top, right, bottom)):
                        tile_type = "r"
                    
                    if right and not any((top,left, bottom)):
                        tile_type = "l"
                    
                    if right and left and not any((top, bottom)):
                        tile_type = "lr"
                    
                    if top and not any((right, left, bottom)):
                        tile_type = "b"

                    if bottom and not any((right, left, top)):
                        tile_type = "t"

                    if bottom and top and not any((right, left)):
                        tile_type = "tb"

                    if left and bottom and not any((top, right)):
                        tile_type = "tr"
                    
                    if right and bottom and not any((top, left)):
                        tile_type = "tl"
                    
                    if left and top and not any((bottom, right)):
                        tile_type = "br"

                    if right and top and not any((bottom, left)):
                        tile_type = "bl"

                    if all((top, bottom, right)) and not left:
                        tile_type = "tbr"

                    if all((top, bottom, left)) and not right:
                        tile_type = "tbl"
                    
                    if all((left, right, top))and not bottom:
                        tile_type = "lrb"
                    
                    if all((left, right, bottom)) and not top:
                        tile_type = "lrt"

                    SoilTile((index_col * TILE_SIZE, index_row * TILE_SIZE), self.soil_surfs[tile_type], [self.all_sprites, self.soil_sprites])
