from OutputFunctions import steer, set_break, set_throttle
from InputFunctions import get_info
import numpy as np
import neuro.visualize as vis
import neat
import os
import time

MAX_ANGLE = 16384
cnt_enabled = False

def set_fitness():
    # todo crazy calculations
    return get_info()[8]  # returns track progress


def control_car(nn_output):
    """evaluates output node with highest confidence,
    multiplies confidence with steer angle of vJoy and controls car"""
    index = np.argmax(nn_output)  # gets index of highest value

    # gets highest value (between 0 and 1) and multiplies with max steer angle
    # to get actual angle which neural network believes is correct
    angle = int(round(MAX_ANGLE * np.amax(nn_output)))  # rounds float to integer

    if index == 0:  # throttle
        set_throttle(angle)
    elif index == 1:  # break
        set_break(angle)
    else:  # steering
        steer(steering=angle)
    # todo multiple outputs instead of steering -> see notes


def evaluate_genomes(genomes, config):
    """creates feed forward neural network, calculates and refreshes fitness and controls car with given output"""
    for genome_id, genome in genomes:  # iterate through all genomes received from population.run
        # create network
        net = neat.nn.FeedForwardNetwork.create(genome, config)  # create feed forward network

        output = np.asarray(  # converts output to numpy array
            net.activate([get_info()[8]]))  # start neural network with given input (track progress)
        genome.fitness = set_fitness()  # fitness function

        control_car(output)  # controls car with every tick


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run until fitness threshold is reached (round on track is completed)
    winner = p.run(evaluate_genomes)

    vis.draw_net(config, winner, True)
    vis.plot_stats(stats, ylog=False, view=True)
    vis.plot_species(stats, view=True)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    if cnt_enabled:
        # 5 sec countdown
        for i in list(range(5))[::-1]:
            print(i + 1)
            time.sleep(1)

    config_path = os.path.join(os.path.dirname(__file__), 'config')
    run(config_path)
