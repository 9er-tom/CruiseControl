from OutputFunctions import steer, usepedals
import numpy as np
from InputFunctions import checkOnTrack, get_car_info
import neat
import time
from neuro.screengrab import grab_screen

prevIndex = -1

def control_car(nn_output):
    """evaluates output node with highest confidence and controls car"""
    nn_output = np.asarray(nn_output)
    index = np.argmax(nn_output)  # gets index of highest value
    # print(index, '\n')

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


def heresy_control(nn_output):
    global prevIndex
    out = np.argmax(nn_output)  # gets index of highest value

    if out != prevIndex:
        print(out, '\n')
        prevIndex = out

    # steer((int(out / 25)) / 20)
    # print((out % 25) / 5)
    # print(((out % 10) % 5) / 5)
    # usepedals(throttle=((out % 10) % 5) / 5, brake=(out % 25) / 5)

    out -= 24
    # steeer = (int(out/5)/4)
    # print("Out",out,"Steer",abs((int(out/5)/4)),"Pedal",(int(round((out/5)-int(out/5),1)*5))/4)
    pedals = (int(round((out / 5) - int(out / 5), 1) * 5)) / 4
    steer(abs((int(out / 5) / 4)) / 3 + (1 / 3))
    usepedals(brake=pedals, throttle=pedals * (-1))


def drive_loop(net):
    """population-member (organism) receives track progress as input and continually uses output to drive until it
    gets off track or stands still too long """
    while checkOnTrack():
        # output = net.activate(image_control())  # uses track map image array as input
        output = net.activate(get_car_info())  # uses car data as input

        # control_car(output)
        heresy_control(np.asarray(output))  # controls car with computed output, see dictionary above


def image_control():
    img_array = grab_screen()
    np.append(img_array, get_car_info()[2])
    return img_array
