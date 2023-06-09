# Goździk the Game - powered by NEAT algorithm


https://user-images.githubusercontent.com/18630618/232147738-85db54da-db5c-47ba-8ad8-950fa2d1542e.mov


## Introduction

I decided to use NEAT (Neuroevolution of augmenting topologies) to teach a Feed Forward neural network model to play a platform game. It connects genetic algorithms with the power of neural networks which I've found fascinating. The notion behind NEAT is to encode neural networks as chromosomes and improve them through evolution using fitness function as a metric. It's a powerful tool for various reinforcement learning tasks.

## NEAT

It was initially introduced in [this paper](https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf) by Kenneth O. Stanley and Risto Miikkulainen from The University of Texas. Basic steps of this algorithm:
1. Start with a population of neural networks with random weights
2. Calculate fitness for every network
3. Crossover best networks with each others
4. Mutate networks with some probability 
    1. Mutate by adding new node 
    2. Mutate by deleting node
    3. Mutate by adding connection
    4. Mutate by deleting connection
5. Run this over many generations to get the best result

In NEAT each chromosome contain two sets of genes.

1. Node genes - storing information about occurrence of neurons
2. Connection genes - storing information about connections between neurones and their wights



## Solution

### Problem we face

- Player (cat) has to avoid obstacles (snails or flies)
- Every avoided obstacle is a 1 point
- Player can only jump
- Obstacles are chosen randomly
- Speed (velocity) of obstacles is also random for every obstacle

### Fitness function

My proposed fitness function evaluates player (neural network/chromosome) by following critiera:

- For every frame the player is alive +0.1
- For every obstacle the player avoided +5
- Every time player hits the obstacle -1 and we terminate this solution

### Neural network

**Features I choose:**

- Next obstacle Y-axis value
- Distance between the player and the very next obstacle
- Velocity the next obstacle is coming
- Type of the next obstacle (0 - snail, 1 - fly)

I also decided to use MinMax scaler on numeric features. <ins>It really improved the results</ins>.

**Important initial parameters:**

- Input nodes: 4
- Hidden nodes: 0
- Output nodes: 1
- Activation function: tanh
- Initial connection: full

### Other assumptions

- Max generations: 35
- Max score: 100 (above that solution is perfect, no need to train furthermore)
- Initial population: 30


## Outcome

Here you can see an example video of a training process in 100 fps: [training video](https://drive.google.com/file/d/1tHEzR1QgJQNCuksQWjOaAwxA3iNuoEtP/view?usp=share_link)
It took it 6 generations to master the game this time.

Below is a neural network our algorithm found works best for this problem. I save it as a pickle file in models/best_model.pickle.

<a href="https://imgbb.com/"><img src="https://i.ibb.co/W5tqBpn/Digraph-gv.png" alt="Digraph-gv" border="0"></a>

Here you can check out our trained network playing the game by it's own.

[![test ai](https://s11.gifyu.com/images/test.gif)](https://user-images.githubusercontent.com/18630618/232147738-85db54da-db5c-47ba-8ad8-950fa2d1542e.mov)

## Setting up

1. ```git clone https://github.com/Ilnicki010/neat-ai-python-game.git```
2. ```cd neat-ai-python-game```
3. ```pip install -r requirements.txt```
4. ```python main.py```

## Future development

My list of ideas to improve in a neuroevolution:
- Make game more complex (maybe sth like Mario or Donkey Kong)
- Try to do a multiplayer game (many AIs fight with each other)
- Neuroevolution = many neural networks = many simulations = computing power. Read more about running these in parallel, optimize, run on Azure, etc.
