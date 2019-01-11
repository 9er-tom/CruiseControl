import neuro.controller as control
from InputFunctions import get_car_info, get_lap_info, resetflyinglap, reset_time
from OutputFunctions import kill, usepedals, capture_replay
# import neuro.visualize as vis
import neat
import os
import time
import datetime

countdown_enabled = True

# ----- Checkpoint parameters  ----- #
CHECKPOINT_PREFIX = 'cp-'  # prefix of checkpoint files
checkpoint_interval = 5  # numbers of generation after which a checkpoint is saved
dir_name = 'training-' + datetime.datetime.today().strftime('%Y-%m-%d_%Hh-%Mm-%Ss')  # checkpoint directory name


def evaluate_genomes(genomes, config):
    """creates feed forward neural network, calculates and refreshes fitness and controls car with given output"""
    for genome_id, genome in genomes:  # iterate through all genomes received from population.run
        print('Organism: ', genome_id)
        # create network
        net = neat.nn.FeedForwardNetwork.create(genome, config)  # create feed forward network

        resetflyinglap()  # resets flying start counter
        reset_time()

        usepedals(throttle=1)
        time.sleep(0.5)
        control.drive_loop(net)  # starts driving loop

        genome.fitness = -1 if set_fitness() == 0 else set_fitness()  # fitness function

        # genome.fitness = set_fitness()
        print('Fitness: ', genome.fitness, '\n')

        kill()  # resets car
        # vis.draw_net(config, genome, True)


def set_fitness():
    """fitness function
    returns fitness for current organism"""
    # current lap (0 if flying start) + track progress - reset position (differs for each track)
    return get_car_info()[3] + get_lap_info()[3] - 0.81


def check_checkpoint(config):
    """Returns the population of the specified checkpoint or creates a new one if no name is specified is found.
    If given name cannot be found, exception is thrown"""
    checkpoint_name = input('Path to checkpoint to load (none if blank): ')
    if len(checkpoint_name) != 0:  # loads specified checkpoint population
        print('Loading checkpoint...')
        return neat.Checkpointer.restore_checkpoint(checkpoint_name)
    else:  # creates new population
        return neat.Population(config)


def run(config_file):
    """starts neural network"""
    global dir_name
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = check_checkpoint(config)  # create or load population

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # creates checkpoint after set number of generations or after 5 minutes (default NEAT settings)
    # creates directory for every day in which checkpoints are saved

    # delete empty directories
    dirs = os.walk('.')
    for d in dirs:
        if not d[2]:
            os.rmdir(d[0])

    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    p.add_reporter(neat.Checkpointer(checkpoint_interval, filename_prefix=dir_name + '/' + CHECKPOINT_PREFIX))

    # Starts countdown, if enabled
    if countdown_enabled:
        # 5 sec countdown
        for i in list(range(3))[::-1]:
            print(i + 1)
            time.sleep(1)
    # Run until fitness threshold is reached (round on track is completed)
    winner = p.run(evaluate_genomes)
    capture_replay()

    # visualize winning genome
    # vis.draw_net(config, winner, True)
    # vis.plot_stats(stats, ylog=False, view=True)
    # vis.plot_species(stats, view=True)

    # # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), 'config')  # loads config from same dir this file is in
    run(config_path)
