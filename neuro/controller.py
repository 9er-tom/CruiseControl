from OutputFunctions import steer, usepedals
import numpy as np
import socket
import pickle
from InputFunctions import checkOnTrack, get_car_info
import neat
import time


def control_car(nn_output):
    """evaluates output node with highest confidence and controls car"""
    nn_output = np.asarray(nn_output)
    index = np.argmax(nn_output)  # gets index of highest value
    # print(index, '\n')

    # throttle
    if index == 0:
        usepedals(throttle=0.2)
    elif index == 1:
        usepedals(throttle=0.4)
    elif index == 2:
        usepedals(throttle=0.6)
    elif index == 3:
        usepedals(throttle=0.8)
    elif index == 4:
        usepedals(throttle=1.0)

    # brake
    elif index == 5:
        usepedals(brake=0.2)
    elif index == 6:
        usepedals(brake=0.4)
    elif index == 7:
        usepedals(brake=0.6)
    elif index == 8:
        usepedals(brake=0.8)
    elif index == 9:
        usepedals(brake=1.0)

    # steering left
    elif index == 10:
        steer(0.0)
    elif index == 11:
        steer(0.2)
    elif index == 12:
        steer(0.3)
    elif index == 13:
        steer(0.4)

    # steer center
    elif index == 14:
        steer(0.5)

    # steering right
    elif index == 15:
        steer(0.6)
    elif index == 16:
        steer(0.7)
    elif index == 17:
        steer(0.8)
    elif index == 18:
        steer(0.9)
    elif index == 19:
        steer(1.0)


def heresy_control(out):
    nn_output = np.asarray(out)
    out = np.argmax(nn_output)  # gets index of highest value
    # print(index, '\n')

    steer((int(out / 25)) / 20)
    # print((out % 25) / 5)
    # print(((out % 10) % 5) / 5)
    usepedals(throttle=((out % 10) % 5) / 5, brake=(out % 25) / 5)


def drive_loop(net):
    """population-member (organism) receives track progress as input and continually uses output to drive until it
    gets off track or stands still too long """
    while checkOnTrack():
        net_input = get_car_info().tolist()
        output = net.activate(net_input)  # uses track progress as input
        heresy_control(output)  # controls car with computed output, see dictionary above
