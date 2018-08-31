import neuro.controller as control
from InputFunctions import get_info, resetflyinglap, reset_time
from OutputFunctions import kill
import neuro.visualize as vis
import neat
import os
import time
import datetime

cnt_enabled = True  # countdown
CHECKPOINT_PREFIX = 'neat-checkpoint-'  # prefix of checkpoint files

# ------- checkpoint parameters ------- #
checkpoint_interval = 10  # numbers of generation after which a checkpoint is saved
load_checkpoint = False  # if this is true the most current checkpoint is loaded
load_specific_checkpoint = False  # if this is True...
specific_checkpoint = 'training-31-8-18/neat-checkpoint-129'  # ... this specific checkpoint is loaded

dir_name = datetime.datetime.today().strftime('%Y-%m-%d')  # format of checkpoint directory name


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

        genome.fitness = set_fitness()  # fitness function TODO update fitness every tick
        print('Fitness: ', genome.fitness, '\n')

        # vis.draw_net(config, genome, True)


def set_fitness():
    """fitness function
    returns fitness for current organism"""
    # current lap (0 if flying start) + track progress - reset position (differs for each track)
    return get_info()[9] + get_info()[13] - 0.81


def check_checkpoint(config):
    """Checks directory for neat-checkpoints.
    Returns the population of the latest checkpoints or creates a new one of no checkpoint is found"""
    checkpoint_list = []  # list containing checkpoint files

    for string in os.listdir('.'):  # for every file in directory TODO search for most current directory
        if CHECKPOINT_PREFIX in string:  # if file name contains specified prefix
            checkpoint_list.append(  # identifying number of checkpoint gets added to list
                int(string[string.rfind('-') + 1:]))  # searches for last occuring dash (-) and gets following digits
    if not checkpoint_list:  # checks if list is empty in ultra pythonic way (if a list is empty it returns false)
        print("No checkpoint found, starting anew...")
        return neat.Population(config)

    checkpoint_number = str(max(checkpoint_list))  # get highest identifying number of checkpoint files
    print("Loading checkpoint ", checkpoint_number)
    return neat.Checkpointer.restore_checkpoint(
        CHECKPOINT_PREFIX + checkpoint_number)  # loads checkpoint file with highest number


def run(config_file):
    """starts neural network"""
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    if load_checkpoint:  # loads population from checkpoint if flag is set
        if load_specific_checkpoint:  # if flag is set, specific checkpoint is loaded
            p = neat.Checkpointer.restore_checkpoint(specific_checkpoint)
        else:  # otherwise most recent checkpoint is loaded
            p = check_checkpoint(config)
    else:  # create new population if checkpoint is not loaded
        p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # creates checkpoint after set number of generations or after 5 minutes (default NEAT settings)
    # creates directory for every day in which checkpoints are saved
    if not os.path.isdir(dir_name):  # TODO multiple dirs for same day
        os.mkdir(dir_name)
    p.add_reporter(neat.Checkpointer(checkpoint_interval, filename_prefix=dir_name + '/' + CHECKPOINT_PREFIX))

    # # Run until fitness threshold is reached (round on track is completed)
    # winner = p.run(evaluate_genomes)

    # # visualize winning genome
    # vis.draw_net(config, winner, True)
    # vis.plot_stats(stats, ylog=False, view=True)
    # vis.plot_species(stats, view=True)

    # # Display the winning genome.
    # print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    if cnt_enabled:
        # 5 sec countdown
        for i in list(range(3))[::-1]:
            print(i + 1)
            time.sleep(1)

    config_path = os.path.join(os.path.dirname(__file__), 'config')  # loads config from same dir this file is in
    run(config_path)
