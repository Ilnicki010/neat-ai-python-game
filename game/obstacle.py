import pygame
from random import choice
from enum import Enum
import os


class ObstacleTypeEnum(Enum):
    snail = 0
    fly = 1


class Obstacle:
    def __init__(self, x: float, base_height: int, velocity: int):
        self.x = x
        self.type: ObstacleTypeEnum = choice(list(ObstacleTypeEnum))
        self.img = self.set_img_by_type()
        self.y = self.set_y_by_type(base_height)
        self.passed = False
        self.velocity = velocity

    def set_img_by_type(self):
        if self.type == ObstacleTypeEnum.snail:
            return pygame.transform.scale2x(pygame.image.load(f"{os.getcwd()}/game/imgs/snail1.png").convert_alpha())
        else:
            return pygame.transform.scale2x(pygame.image.load(f"{os.getcwd()}/game/imgs/fly.png").convert_alpha())

    def set_y_by_type(self,base_height):
        if self.type == ObstacleTypeEnum.snail:
            return base_height - self.img.get_height()
        else:
            return base_height - self.img.get_height() - 90

    def move(self):
        self.x -= self.velocity

    def collide(self, player, screen):
        player_mask = player.get_mask()
        obstacle_mask = pygame.mask.from_surface(self.img)

        offset = (self.x - player.x, self.y - player.y + self.img.get_height())

        c_point = player_mask.overlap(obstacle_mask, offset)

        if c_point:
            return True

        return False

    def draw(self, screen):
        if self.type == ObstacleTypeEnum.snail:
            screen.blit(self.img, (self.x, self.y))
        else:
            screen.blit(self.img, (self.x, self.y))
