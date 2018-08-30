import pyvjoy
import pynput
import time


'''def steer(steering=0):  # -16384 = links  0 = mitte 16384 = rechts
    print("Steer")
    print(steering)
    steering += 16384
    j.set_axis(pyvjoy.HID_USAGE_X, steering)
    return steering'''

def steer(steering=0.5):  # 0 = links  0.5 = mitte 1 = rechts
    j.set_axis(pyvjoy.HID_USAGE_X, steering*32768)
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


def usepedals(clutch=0.0, brake=0.0, throttle=0.0):
    j.set_axis(pyvjoy.HID_USAGE_Y, throttle*32768)
    j.set_axis(pyvjoy.HID_USAGE_RX, brake*32768)
    j.set_axis(pyvjoy.HID_USAGE_RY, clutch*32768)
    return 0


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


def exitbox(track='ks_zandvoort', car='ks_bmw_m235i_racing'): #teilweise noch nach altem prinzip
    if track == 'ks_zandvoort':
        if car == 'ks_bmw_m235i_racing':
            c = 1
            steer(0)
            usepedals(c, 0, 0.1220703125)
            shift(1)
            time.sleep(5)
            while c > 0:
                c -= 0.0001
                usepedals(c, 0, 0.1220703125)
                time.sleep(0.0005)
            time.sleep(0.5)
            x = 0
            while x > -3500:
                x -= 10
                steer(x)
                time.sleep(0.0005)
            time.sleep(1)

            while x < 1:
                x += 10
                steer(x)
                time.sleep(0.0005)
            time.sleep(2.2)

            while x < 3500:
                x += 10
                steer(x)
                time.sleep(0.0005)
            time.sleep(0.57)

            while x > -1:
                x -= 10
                steer(x)
                time.sleep(0.0005)

    return 0


def kill(way='restart'):
    if way == 'restart':
        k.press(pynput.keyboard.Key.ctrl_l)
        k.press('n')
        time.sleep(0.02)
        k.release('n')
        k.release(pynput.keyboard.Key.ctrl_l)
        time.sleep(3)
        exitboxmenu()
    elif way == 'box':
        k.press(pynput.keyboard.Key.ctrl_l)
        k.press('b')
        time.sleep(0.02)
        k.release('b')
        k.release(pynput.keyboard.Key.ctrl_l)
        time.sleep(3)
        exitbox()
    return 0


def exitboxmenu():
    m.position = (50, 170)
    m.press(pynput.mouse.Button.left)
    time.sleep(0.02)
    m.release(pynput.mouse.Button.left)
    return 0


j = pyvjoy.VJoyDevice(1)
k = pynput.keyboard.Controller()
m = pynput.mouse.Controller()

j.reset()
j.update()
steer(0)

if __name__ == '__main__':
    time.sleep(2)
    kill()
    j.reset()
