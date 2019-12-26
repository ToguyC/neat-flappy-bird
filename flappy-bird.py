# see: https://neat-python.readthedocs.io/en/latest/config_file.html
#      http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf

import pygame
import neat
import time
import os
import gzip
import random
from Bird import Bird
from Pipe import Pipe
from Base import Base

WIDTH, HEIGHT = 550, 800

pygame.init()
pygame.font.init()

# Load all images.
# scale2x is to double the size of the image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bg.png')))

STAT_FOND = pygame.font.SysFont('comicsans', 50)

GEN = 0

def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.show(win)
    base.show(win)
    for bird in birds:
        bird.show(win)

    text = STAT_FOND.render(f'Score: {str(score)}', 1, (255, 255, 255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))

    text = STAT_FOND.render(f'Gen: {str(gen)}', 1, (255, 255, 255))
    win.blit(text, (10, 10))

    pygame.display.flip()

def main(genomes, config):
    global GEN
    GEN += 1
    networks = []
    genome = []
    birds = []

    for _, g in genomes:
        network = neat.nn.FeedForwardNetwork.create(g, config)
        networks.append(network)
        birds.append(Bird(230, 350))
        g.fitness = 0
        genome.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            run = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            genome[i].fitness += 0.1

            outputs = networks[i].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if outputs[0] > 0.5:
                bird.jump()

        add_pipe = False
        removed = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    genome[i].fitness -= 1
                    birds.pop(i)
                    networks.pop(i)
                    genome.pop(i)

                if not pipe.passed and pipe.x + pipe.PIPE_TOP.get_width() < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in removed:
            pipes.remove(r)

        for i, bird in enumerate(birds):
            if genome[i].fitness >= 20:
                run = False
                break

            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(i)
                networks.pop(i)
                genome.pop(i)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)

        clock.tick(30)

def run(config_path, model=None):
    import pickle
    
    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)

    if model:
        population = model

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer())
    winner = population.run(main)

    # Save the current simulation state
    filename = 'max-threshold-1'
    print(f'Saving checkpoint to {filename}')
    with open(filename, 'wb') as f:
        pickle.dump(population, f)

if __name__ == "__main__":
    import pickle

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    if os.path.exists(os.path.join(local_dir, 'max-threshold-1')):
        with open('max-threshold-1', 'rb') as f:
            model = pickle.load(f)
        run(config_path, model=model)
    else:
        run(config_path)