import os
import sys
import platform
import numpy
from sim_info import info
import time

cnt_enabled = False  # countdown

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
    return [info.physics.gear,
            info.physics.rpms,
            info.physics.speedKmh,
            info.physics.wheelSlip,
            info.physics.wheelLoad,
            info.physics.tyreCoreTemperature,
            info.physics.kersCharge,
            info.physics.numberOfTyresOut,
            info.physics.tyreDirtyLevel,
            info.graphics.carCoordinates,
            info.graphics.normalizedCarPosition,
            info.graphics.iCurrentTime,
            info.graphics.iLastTime,
            info.graphics.iBestTime,
            info.static.carModel,
            info.static.track
            ]



def checkOnTrack():
    """checks if car is on track by evaluating damage and dirt levels of tyre\n
        returns true if car is on track"""
    return (info.physics.numberOfTyresOut <= 0
            and numpy.sum(info.physics.tyreDirtyLevel) <= 0.05
            and numpy.sum(info.physics.carDamage) <= 0.05)


# onTrack = 1  # assuming car is on track and trying to disprove that
# if info.physics.numberOfTyresOut > 0:
#     onTrack = 0
# if numpy.sum(info.physics.tyreDirtyLevel) > 0.05:
#     onTrack = 0
# if numpy.sum(info.physics.carDamage) > 0.05:
#     onTrack = 0
# return onTrack


if __name__ == '__main__':

    if cnt_enabled:
        # 5 sec countdown
        for i in list(range(5))[::-1]:
            print(i + 1)
            time.sleep(1)
    while True:  # displays track info every 0.5 seconds
        time.sleep(0.5)
        print(get_info())
