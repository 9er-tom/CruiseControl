from __future__ import division

import os
import sys
import platform
import numpy
from sim_info import info

cnt_enabled = False  # countdown
flyingstart = 0
lastabpos = info.graphics.normalizedCarPosition
lasttime = info.graphics.iCurrentTime
timewaiting = 0

if platform.architecture()[0] == "64bit":
    sysdir = "stdlib64"
else:
    sysdir = "stdlib"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "my_super_app_lib", sysdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

myprogress = info.graphics.normalizedCarPosition


# car = info.static.carModel
# track = info.static.track


# def get_session_info():
#   return car, track

def get_car_position():
    return info.graphics.normalizedCarPosition

def get_game_time():
    return info.graphics.iCurrentTime

def get_info():
    position = info.graphics.normalizedCarPosition
    global flyingstart
    # print(flyingstart)  # testing purposes
    # if flyingstart > 0 and 0 < position < 10:
    #   flyingstart = 0
    wload = info.physics.wheelLoad
    return numpy.array([  # info.physics.gear,
        # info.physics.rpms,
        info.physics.speedKmh],  # Topspeed 250
        # info.physics.wheelSlip,
        # wload[0], wload[1], wload[2], wload[3]],
        # info.physics.tyreCoreTemperature,
        # info.physics.kersCharge,
        # checkOnTrack(),
        # info.graphics.carCoordinates,
        # info.graphics.normalizedCarPosition],
        # info.graphics.iCurrentTime,
        # info.graphics.iLastTime,
        # info.graphics.iBestTime,
        # info.graphics.numberOfLaps - flyingstart,
        # info.static.carModel,
        # info.static.track],
        dtype=float)

def get_speed():
    return info.physics.speedKmh

def checkOnTrack():
    global timewaiting
    printcurrtime()
    """checks if car is on track by evaluating damage and dirt levels of tyre\n
            returns true if car is on track"""
    # rightnow =  time.time()
    # if info.physics.speedKmh > 5:
    #    timewaiting = rightnow
    # print(timewaiting)
    return (info.physics.numberOfTyresOut <= 0
            and numpy.sum(info.physics.tyreDirtyLevel) <= 0.05
            and numpy.sum(info.physics.carDamage) <= 0.05
            and info.graphics.isInPit <= 0
            and info.graphics.completedLaps < 1
            and info.physics.speedKmh > 0.01
            )  # and rightnow - timewaiting <= 5)

    # onTrack = 1  # assuming car is on track and trying to disprove that
    # if info.physics.numberOfTyresOut > 0:
    #     onTrack = 0
    # if numpy.sum(info.physics.tyreDirtyLevel) > 0.05:
    #     onTrack = 0
    # if numpy.sum(info.physics.carDamage) > 0.05:
    #     onTrack = 0
    # if info.graphics.isInPit > 0:
    #     onTrack = 0
    # return onTrack


def getdistance():
    global flyingstart
    global lastabpos
    mycurrposition = info.graphics.normalizedCarPosition
    if (flyingstart != 1 and mycurrposition < 0.5):
        flyingstart = 1
    mycurrposition+=flyingstart
    distance = mycurrposition - lastabpos
    lastabpos = mycurrposition
    return distance


'''def calculatereward():
    global flyingstart
    global lastabpos
    global lasttime
    nowtime = info.graphics.iCurrentTime/1000.0
    reltime = nowtime - lasttime
    lasttime = nowtime
    pos = info.graphics.normalizedCarPosition
    spd =  info.physics.speedKmh
    abpos = (flyingstart + pos) * 1000000
    relpos = abpos - lastabpos
    lastabpos = abpos
    #print("relpos:",relpos,"\nabpos:",abpos,"\nlaspos:",lastabpos)

    if(pos < 0.5):
        flyingstart = 1
    if(reltime > 0):
        reward = relpos - reltime
    else:
        reward = relpos
    #if(spd >= 0.5):
        #reward = relpos -
    #else:
        #eward = -0.5
    #reward = reward - (info.graphics.iCurrentTime / 200000)
    return reward'''


def calculatereward():
    #global lasttime
    #currenttime = info.graphics.iCurrentTime
    r = (getdistance() - 0.000000001) #/ ((currenttime - lasttime))
    #if(currenttime < lasttime):
    #    r=(getdistance() - 0.000000001) / (currenttime)
    #lasttime = currenttime
    return r


def resetflyinglap():
    global flyingstart
    flyingstart = 0
    return 0


def getpos():
    return info.graphics.normalizedCarPosition


def getlaps():
    return info.graphics.completedLaps

def getbestlap():
    return info.graphics.iBestTime

def printcurrtime():
    print(info.graphics.iCurrentTime,"    ",info.graphics.currentTime)


if __name__ == '__main__':
    while True:
        print(info.graphics.iCurrentTime)
