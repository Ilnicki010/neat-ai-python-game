import pygame
import os


class Base:
    def __init__(self, y: float, velocity: int):
        self.img = pygame.transform.scale2x(pygame.image.load(f"{os.getcwd()}/game/imgs/base.png").convert_alpha())
        self.width = self.img.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.width
        self.velocity = velocity

    def move(self):

        self.x1 -= self.velocity
        self.x2 -= self.velocity
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, screen):

        screen.blit(self.img, (self.x1, self.y))
        screen.blit(self.img, (self.x2, self.y))
