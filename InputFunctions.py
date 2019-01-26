import os
import sys
import platform
import numpy
from sim_info import info

cnt_enabled = False  # countdown
flyingstart = 0
lastabpos = info.graphics.normalizedCarPosition * 1000000
lasttime = info.graphics.iCurrentTime / 1000.0
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

def get_info():
    position = info.graphics.normalizedCarPosition
    global flyingstart
    # print(flyingstart)  # testing purposes
    # if flyingstart > 0 and 0 < position < 10:
    #   flyingstart = 0
    wload = info.physics.wheelLoad
    return numpy.array([  # info.physics.gear,
        # info.physics.rpms,
        round(info.physics.speedKmh) / 250],  # Topspeed 250
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
        dtype=object)


def checkOnTrack():
    global timewaiting
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
    global myprogress
    mycurrposition = info.graphics.normalizedCarPosition
    if (mycurrposition - myprogress >= 0):
        nompos = mycurrposition - myprogress
    else:
        nompos = 0
    myprogress = mycurrposition
    if (flyingstart > 0 and nompos >= 0):
        flyingstart = 0

    distance = round(nompos, 5)  # tracke jetzt nur fortschritt (info.graphics.numberOfLaps - flyingstart) +

    # fehlt noch die Zeit abs(info.graphics.numberOfLaps - flyingstart-(info.graphics.iCurrentTime)) #Zeit in Milllisekunden
    return distance


def calculatereward():
    global flyingstart
    global lastabpos
    global lasttime
    nowtime = info.graphics.iCurrentTime / 1000.0
    reltime = nowtime - lasttime
    lasttime = nowtime
    pos = info.graphics.normalizedCarPosition
    spd = info.physics.speedKmh
    abpos = (flyingstart + pos) * 1000000
    relpos = abpos - lastabpos
    lastabpos = abpos
    # print("relpos:",relpos,"\nabpos:",abpos,"\nlaspos:",lastabpos)

    if (pos < 0.5):
        flyingstart = 1
    if (reltime > 0):
        reward = relpos - reltime
    else:
        reward = relpos
    # if(spd >= 0.5):
    # reward = relpos -
    # else:
    # eward = -0.5
    # reward = reward - (info.graphics.iCurrentTime / 200000)
    return reward


def resetflyinglap():
    global flyingstart
    flyingstart = 0
    return 0


def getpos():
    return info.graphics.normalizedCarPosition


def getlaps():
    return info.graphics.completedLaps


if __name__ == '__main__':

    if cnt_enabled:
        # 5 sec countdown
        '''for i in list(range(5))[::-1]:
            print(i + 1)
            time.sleep(1)'''
    totalreward = 0
    while (getlaps() < 1):
        reward = calculatereward()
        print(reward)
        totalreward += reward
    print("Total Reward: ", totalreward)
