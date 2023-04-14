import neat
import numpy as np


def build_ff_network(solution: neat.genome.DefaultGenome, config: neat.config.Config) -> neat.nn.FeedForwardNetwork:
    net = neat.nn.FeedForwardNetwork.create(solution, config)

    return net


def min_max_scale(x: list[float]) -> list[float]:
    return (x - np.amin(x)) / (np.amax(x) - np.amin(x))

def prepare_features(obstacle_y: float, dist_from_obstacle: float, obstacle_velocity: int, obstacle_type: int) -> list[float]:
    x_values_numeric = [
        obstacle_y,
        dist_from_obstacle,
        obstacle_velocity
    ]
    x_values_categorical = [obstacle_type]

    # MinMax scale for better neural network results
    x_scaled = min_max_scale(x_values_numeric)

    return [*x_scaled,*x_values_categorical]