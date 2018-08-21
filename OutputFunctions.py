import pyvjoy
import time


def steer(steering=0):  # -16384 = links  0 = mitte 16384 = rechts
    print("Steer")
    print(steering)
    # steering += 16384
    j.set_axis(pyvjoy.HID_USAGE_X, steering)
    return steering


def shift(gear=0):  # 0 = Neutral#
    j.set_button(1, 0)
    j.set_button(2, 0)
    j.set_button(3, 0)
    j.set_button(4, 0)
    j.set_button(5, 0)
    j.set_button(6, 0)
    j.set_button(7, 0)
    j.set_button(8, 0)  # reverse
    print("Reset Confirm")

    time.sleep(0.01)

    if gear != 0:
        j.set_button(gear, 1)
        print("Shift")
        print(gear)
        print('\n')

    return gear


def usepedals(clutch=0, brake=0, throttle=0):
    j.set_axis(pyvjoy.HID_USAGE_Y, throttle)
    j.set_axis(pyvjoy.HID_USAGE_RX, brake)
    j.set_axis(pyvjoy.HID_USAGE_RY, clutch)
    return 0


def set_throttle(i):
    j.set_axis(pyvjoy.HID_USAGE_Y, i)


def set_break(i):
    j.set_axis(pyvjoy.HID_USAGE_RX, i)


def manageBoost(addsub):  # 1 = +  2 = -
    if addsub == 1:
        j.set_button(15, 1)
        j.update()
    elif addsub == 2:
        j.set_button(16, 1)
        j.update()

    j.set_button(15, 0)
    j.set_button(16, 0)
    j.update()
    return 0


def manageBrakeBalance(addsub):  # 1 = Front+  2 = Back+
    if addsub == 1:
        j.set_button(17, 1)
        j.update()
    elif addsub == 2:
        j.set_button(18, 1)
        j.update()

    j.set_button(17, 0)
    j.set_button(18, 0)
    j.update()
    return 0


def manageKERS(addsub):  # 1 = activate KERS
    if addsub:
        j.set_button(19, 1)
    else:
        j.set_button(19, 0)
    j.update()
    return 0


def manageDRS(addsub):  # 1 = activate DRS
    if addsub:
        j.set_button(20, 1)
    else:
        j.set_button(20, 0)
    j.update()
    return 0


def reset():
    j.reset()
    j.update()
    return 0


j = pyvjoy.VJoyDevice(1)

j.reset()
j.update()
if __name__ == '__main__':
    # 5 sec countdown
    for i in list(range(2))[::-1]:
        print(i + 1)
        time.sleep(1)
    steer(16000)
