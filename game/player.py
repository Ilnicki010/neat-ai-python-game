import pygame
import os

class Player:
    VELOCITY = 9
    MASS = 1

    def __init__(self, x: float, y: float):
        self.img = pygame.transform.scale2x(pygame.image.load(f"{os.getcwd()}/game/imgs/cat.png").convert_alpha())
        self.is_jump = False
        self.jump_count = 0
        self.x = x
        self.y = y
        self.height = self.y
        self.velocity = self.VELOCITY
        self.mass = self.MASS
        self.tick_count = 0

    def jump(self):
        self.jump_count += 1
        self.is_jump = True

    def move(self):
        if self.is_jump:
            # calculate force (F)
            F = (1 / 2) * self.mass * (self.velocity ** 2)

            self.y -= F
            self.velocity = self.velocity - 1

            # object reached its maximum height
            if self.velocity < 0:
                self.mass = -1

            # objected reaches its original state
            if self.velocity == -self.VELOCITY - 1:
                self.is_jump = False

                self.velocity = self.VELOCITY
                self.mass = self.MASS

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y - self.img.get_height()))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
