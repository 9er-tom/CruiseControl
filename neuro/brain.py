import neuro.controller as control
from InputFunctions import get_info, resetflyinglap, reset_time
from OutputFunctions import kill
import neuro.visualize as vis
import neat
import os
import time

MAX_ANGLE = 16384
cnt_enabled = True  # countdown


def evaluate_genomes(genomes, config):
    """creates feed forward neural network, calculates and refreshes fitness and controls car with given output"""
    for genome_id, genome in genomes:  # iterate through all genomes received from population.run
        print('Organism: ', genome_id)
        # create network
        net = neat.nn.FeedForwardNetwork.create(genome, config)  # create feed forward network

        resetflyinglap()  # resets flying start counter
        reset_time()
        control.drive_loop(net)  # starts driving loop
        kill()  # resets car

        genome.fitness = set_fitness()  # fitness function
        print('Fitness: ', genome.fitness, '\n')

        # vis.draw_net(config, genome, True)


def set_fitness():
    return get_info()[9] + get_info()[13] - 0.81
    # return get_info()[10]  # returns track progress


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
    p.add_reporter(neat.Checkpointer(10))

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
        for i in list(range(3))[::-1]:
            print(i + 1)
            time.sleep(1)

    config_path = os.path.join(os.path.dirname(__file__), 'config')
    run(config_path)
