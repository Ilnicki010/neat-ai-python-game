import pygame
from .base import Base
from .player import Player
from .obstacle import Obstacle
from random import randint

pygame.init()
pygame.display.set_caption("Goździk the Game")
pygame.font.init()

class Game:
    MAIN_FONT = pygame.font.SysFont("vt323", 40)
    WHITE = (255, 255, 255)
    BLUE = (135, 206, 250)

    def __init__(self, screen, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.base_height = window_height - 150

        self.players = [Player(100, self.base_height)]
        self.obstacles = [Obstacle(self.window_width, self.base_height, randint(10, 20))]
        self.base = Base(self.base_height, 10)

        self.next_obstacle_idx = 0
        self.add_obstacle = False

        self.generation_idx = 0
        self.score = 0
        self.screen = screen

    def draw_window(self):
        self.screen.fill(self.BLUE)
        self.base.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for player in self.players:
            player.draw(self.screen)

        score_label = self.MAIN_FONT.render("score: " + str(self.score), True, self.WHITE)
        self.screen.blit(score_label, (self.window_width - score_label.get_width() - 15, 10))

        score_label = self.MAIN_FONT.render("generation: " + str(self.generation_idx - 1), True , self.WHITE)
        self.screen.blit(score_label, (10, 10))

        score_label = self.MAIN_FONT.render("no. alive: " + str(len(self.players)), True, self.WHITE)
        self.screen.blit(score_label, (10, 50))

        # pygame.display.update()

    def reset(self):
        self.score = 0
        self.obstacles = [Obstacle(self.window_width, self.base_height, randint(10, 20))]
        self.players = [Player(100, self.base_height)]
        self.base = Base(self.base_height, 10)

        self.next_obstacle_idx = 0
        self.add_obstacle = False

    def loop(self):
        self.base.move()
        self.add_obstacle = False
        obstacles_to_remove = []
        self.next_obstacle_idx = 0

        for player in self.players:
            player.move()

        for obstacle in self.obstacles:
            obstacle.move()
            for player in self.players:
                if not obstacle.passed and obstacle.x < player.x:
                    obstacle.passed = True
                    self.add_obstacle = True

            if obstacle.x + obstacle.img.get_width() < 0:
                obstacles_to_remove.append(obstacle)

        if self.add_obstacle:
            self.score += 1
            self.obstacles.append(Obstacle(self.window_width, self.base_height, randint(10, 20)))

        for obstacle in obstacles_to_remove:
            self.obstacles.remove(obstacle)

        if len(self.players) > 0 and len(self.obstacles) > 1 and self.players[0].x > self.obstacles[0].x + self.players[
            0].img.get_width():  # determine whether to use the first or second obstacle
            self.next_obstacle_idx = 1

