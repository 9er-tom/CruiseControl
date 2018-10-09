import OutputFunctions
import InputFunctions
import time


def inputtest(sec=0):
    timeout = time.time() + sec
    while True:
        test = 0
        print(InputFunctions.get_car_info())
        if test == 5 or time.time() > timeout:
            break
        test = test - 1
    return 0


def steertest():
    # for l in list(range(4))[::-1]:
    #     print(l + 1)
    #     time.sleep(1)

    x = 0
    while x < 14300:
        x = x + 10
        OutputFunctions.steer(x)
        time.sleep(0.0005)
    time.sleep(2)

    while x > -14300:
        x = x - 10
        OutputFunctions.steer(x)
        time.sleep(0.0005)
    time.sleep(2)

    while x < 1:
        x = x + 10
        OutputFunctions.steer(x)
        time.sleep(0.0005)

    x = 0
    while x < 30000:
        x += 10
        OutputFunctions.usepedals(0, 0, x)
    time.sleep(2)
    OutputFunctions.usepedals()

    x = 0
    c = 0
    while c < 35000:
        c += 30
        OutputFunctions.usepedals(c, 0, 0)
    while x < 9:
        OutputFunctions.shift(x)
        x += 1
        time.sleep(2)
    while c > 0:
        c -= 30
        OutputFunctions.usepedals(c, 0, 0)
    OutputFunctions.shift()
    return 0


for i in list(range(4))[::-1]:
    OutputFunctions.reset()
    print("steer")
    print(i + 1)
    time.sleep(1)

# steertest()
# inputtest(2000000)


x = 0
while x < 1:
    x = x + 0.05
    OutputFunctions.steer(x)
    time.sleep(0.05)
x = 0
OutputFunctions.reset()

print("throttle")
time.sleep(2)

while x < 1:
    x = x + 0.05
    OutputFunctions.usepedals(0.0, 0.0, x)
    time.sleep(0.05)
x = 0

print("brake")
time.sleep(2)

while x < 1:
    x = x + 0.05
    OutputFunctions.usepedals(0.0, x, 0.0)
    time.sleep(0.05)
x = 0

print("clutch")
time.sleep(2)

while x < 1:
    x = x + 0.05
    OutputFunctions.usepedals(x, 0.0, 0.0)
    time.sleep(0.05)
x = 0
# while 1:
#    if InputFunctions.checkOnTrack() != 1:
#        InputFunctions.resetflyinglap()
#        OutputFunctions.kill('restart')
# OutputFunctions.reset()
# OutputFunctions.exitbox()
# time.sleep(5)
# OutputFunctions.kill()
# time.sleep(5)
# OutputFunctions.kill('box')
# time.sleep(10)
# OutputFunctions.reset()
