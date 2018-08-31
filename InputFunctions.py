import os
import sys
import platform
import numpy
from sim_info import info
import time

timestamp = 0
cnt_enabled = False  # countdown
flyingstart = 1
timewaiting = 0

if platform.architecture()[0] == "64bit":
    sysdir = "stdlib64"
else:
    sysdir = "stdlib"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "my_super_app_lib", sysdir))
os.environ['PATH'] = os.environ['PATH'] + ";."


# car = info.static.carModel
# track = info.static.track


# def get_session_info():
#   return car, track


def get_info():
    position = info.graphics.normalizedCarPosition
    global flyingstart
    # print(flyingstart)  # testing purposes
    if flyingstart > 0 and 0 < position < 0.1:
        flyingstart = 0
    return numpy.array([info.physics.gear,
                        info.physics.rpms,
                        info.physics.speedKmh,
                        info.physics.wheelSlip,
                        info.physics.wheelLoad,
                        info.physics.tyreCoreTemperature,
                        info.physics.kersCharge,
                        checkOnTrack(),
                        info.graphics.carCoordinates,
                        info.graphics.normalizedCarPosition,
                        info.graphics.iCurrentTime,
                        info.graphics.iLastTime,
                        info.graphics.iBestTime,
                        info.graphics.numberOfLaps + 1 - flyingstart,
                        info.static.carModel,
                        info.static.track], dtype=object)


def checkOnTrack():
    global timewaiting
    """checks if car is on track by evaluating damage and dirt levels of tyre\n
            returns true if car is on track"""
    if info.physics.speedKmh > 0.1:
        timewaiting = time.time()
        # print(time.time() - timewaiting)
    return (info.physics.numberOfTyresOut <= 0
            and numpy.sum(info.physics.tyreDirtyLevel) <= 0.05
            and numpy.sum(info.physics.carDamage) <= 0.05
            and info.graphics.isInPit <= 0
            and time.time() - timewaiting <= 3)

def reset_time():
    global timewaiting
    timewaiting = time.time()


def resetflyinglap():
    flyingstart = 1
    return 0


if __name__ == '__main__':

    if cnt_enabled:
        # 5 sec countdown
        for i in list(range(5))[::-1]:
            print(i + 1)
            time.sleep(1)
    while True:  # displays track info every 0.5 seconds
        time.sleep(1)
        print(get_info())
