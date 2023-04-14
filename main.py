import pickle
import consts
import neat
import pygame
from game.player import Player
from game import Game
import os
import utils
import visualize


class GozdzikGame:
    def __init__(self, width: int, height: int):
        screen = pygame.display.set_mode((width, height))
        self.game = Game(screen, width, height)
        self.screen = screen

    def test_ai(self, neat_network: neat.nn.FeedForwardNetwork) -> None:
        """
        Test single AI by passing a NEAT neural network.
        """
        clock = pygame.time.Clock()
        player = self.game.players[0]  # when we test AI there's only one player
        while True:
            clock.tick(30)
            self.game.loop()

            features = utils.prepare_features(
                self.game.obstacles[self.game.next_obstacle_idx].y,
                abs(player.x - self.game.obstacles[self.game.next_obstacle_idx].x),
                self.game.obstacles[self.game.next_obstacle_idx].velocity,
                self.game.obstacles[self.game.next_obstacle_idx].type.value
            )

            output = neat_network.activate(features)

            if output[0] > 0.5:
                player.jump()

            self.game.draw_window()

            pygame.display.update()

    def eval_genomes(self, solutions, config: neat.config.Config) -> None:
        """
           Training will simulate multiple players within single game instance.
           Each player (neural network) gets a fitness score.
        """

        clock = pygame.time.Clock()
        self.game.generation_idx += 1
        self.game.reset()

        genomes = [t[1] for t in solutions]
        for genome in genomes: genome.fitness = 0
        networks = [utils.build_ff_network(net_config, config) for net_config in genomes]
        self.game.players = [Player(100, consts.BASE_HEIGHT) for _ in range(len(solutions))]

        while len(self.game.players) > 0:
            clock.tick(100)  # high FPS for faster training
            self.game.loop()

            if self.game.score > 100:  # our model is good enough we can stop the game
                break

            for idx, player in enumerate(self.game.players):
                genomes[idx].fitness += 0.1  # increasing fitness every frame it's alive

                # set up features passed to neural network (more info in README)
                features = utils.prepare_features(
                    self.game.obstacles[self.game.next_obstacle_idx].y,
                    abs(player.x - self.game.obstacles[self.game.next_obstacle_idx].x),
                    self.game.obstacles[self.game.next_obstacle_idx].velocity,
                    self.game.obstacles[self.game.next_obstacle_idx].type.value
                )

                output = networks[idx].activate(features)

                if output[0] > 0.5:
                    player.jump()

            for obstacle in self.game.obstacles:
                for player in self.game.players:
                    if obstacle.collide(player, self.screen):
                        idx = self.game.players.index(player)
                        genomes[idx].fitness -= 1
                        networks.pop(idx)
                        genomes.pop(idx)
                        self.game.players.pop(idx)

            if self.game.add_obstacle:
                for genome in genomes:
                    genome.fitness += 5

            self.game.draw_window()

            pygame.display.update()


def test_ai(network: neat.nn.FeedForwardNetwork):
    game = GozdzikGame(consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT)
    game.test_ai(network)


def train_ai(config: neat.config.Config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    game = GozdzikGame(consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT)

    winner = p.run(game.eval_genomes, n=35)

    with open(f"{CWD}/models/best_model.pickle", "wb") as f:
        pickle.dump(winner, f)

    visualize.draw_net(config, winner, node_names=consts.NODE_NAMES)
    visualize.plot_stats(stats, ylog=False, filename=f"{CWD}/graphs/avg_stats.svg")


def main(neat_config_path: str) -> None:
    neat_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                     neat_config_path)

    # train_ai(neat_config)
    with open(f"{CWD}/models/best_model.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = utils.build_ff_network(winner, neat_config)
    test_ai(winner_net)


if __name__ == "__main__":
    CWD = os.getcwd()
    neat_config_path = f"{CWD}/config.txt"
    main(neat_config_path)
