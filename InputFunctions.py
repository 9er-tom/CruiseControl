import os
import sys
import platform
import numpy as np
from sim_info import info
import time

cnt_enabled = False

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
    return np.array([[info.physics.gear, info.physics.rpms],
                     info.physics.speedKmh,
                     info.physics.wheelSlip,
                     info.physics.wheelLoad,
                     info.physics.tyreCoreTemperature,
                     info.physics.kersCharge,
                     info.physics.numberOfTyresOut,
                     info.physics.tyreDirtyLevel,
                     info.graphics.normalizedCarPosition,
                     info.graphics.iCurrentTime,
                     info.graphics.iLastTime,
                     info.graphics.iBestTime,
                     info.static.carModel,
                     info.static.track
                     ])

    # a = (info.physics.gear, info.physics.rpms)
    # a = a + (info.physics.speedKmh,)
    # a = a + (info.physics.wheelSlip,)
    # a = a + (info.physics.wheelLoad,)
    # a = a + (info.physics.tyreCoreTemperature,)
    # a = a + (info.physics.kersCharge,)
    # a = a + (info.physics.numberOfTyresOut,)
    # a = a + (info.physics.tyreDirtyLevel,)
    # a = a + (info.graphics.normalizedCarPosition,)
    # a = a + (info.graphics.iCurrentTime,)
    # a = a + (info.graphics.iLastTime,)
    # a = a + (info.graphics.iBestTime,)
    # a = a + (getsessionInfo(),)
    # return a


if __name__ == '__main__':

    if cnt_enabled:
        # 5 sec countdown
        for i in list(range(5))[::-1]:
            print(i + 1)
            time.sleep(1)
    while True:
        time.sleep(0.5)
        print(get_info()[8])
