from OutputFunctions import steer, usepedals
import time
def control(out):
    steer((int(out/25))/20)
    print((out%25)/5)
    print(((out%10)%5)/5)
    usepedals(throttle=((out%10)%5)/5,brake=(out%25)/5)

#0.0.0,0.0.1,0.0.2,0.0.3,0.0.4,0.1.0,..,0.1.4,20.4.4
#  0  ,  1  ,  2  ,  3  ,  4  ,  5  ,..,  9  ,
#
#gas:   (out%10)%5
#brake: (out%25)/5
#steer: out/25
#10= gerade 0=0%pedal
#5,
#499