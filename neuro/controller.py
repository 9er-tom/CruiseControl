from OutputFunctions import steer, usepedals
import numpy as np
from InputFunctions import checkOnTrack, get_info
import neat

car_controls = {  # dictionary for car controls
    # in per cent
    # throttle
    0: usepedals(throttle=0.2),
    1: usepedals(throttle=0.4),
    2: usepedals(throttle=0.6),
    3: usepedals(throttle=0.8),
    4: usepedals(throttle=1.0),

    # brake
    5: usepedals(brake=0.2),
    6: usepedals(brake=0.4),
    7: usepedals(brake=0.6),
    8: usepedals(brake=0.8),
    9: usepedals(brake=1.0),

    # steer left
    10: steer(-1.0),
    11: steer(-0.66),
    12: steer(-0.33),

    # steer right
    13: steer(0.33),
    14: steer(0.66),
    15: steer(1.0)
}


def control_car(nn_output):
    """evaluates output node with highest confidence and controls car"""
    nn_output = np.asarray(nn_output)
    index = np.argmax(nn_output)  # gets index of highest value
    car_controls.get(index)


def drive_loop(net):
    """population-member (organism) receives track progress as input and continually uses output to drive until it
    gets off track or stands still too long """
    # todo add reset if standing still for too many loop iterations (speed or possibly rpm?)
    while checkOnTrack():
        output = net.activate(get_info()[10])  # uses track progress as input
        control_car(output)  # controls car with computed output, see dictionary above
