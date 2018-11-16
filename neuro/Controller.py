from OutputFunctions import steer, usepedals
import time
def control(out):
    out-=24
    #steeer = (int(out/5)/4)
    #print("Out",out,"Steer",abs((int(out/5)/4)),"Pedal",(int(round((out/5)-int(out/5),1)*5))/4)
    pedals = (int(round((out/5)-int(out/5),1)*5))/4
    steer(abs((int(out/5)/4))/3)
    usepedals(brake=pedals*(-1),throttle=pedals)

    #steer((int(out/25))/20)
    #print((out%25)/5)
    #print(((out%10)%5)/5)
    #usepedals(throttle=((out%10)%5)/5,brake=(out%25)/5)

#0.0.0,0.0.1,0.0.2,0.0.3,0.0.4,0.1.0,..,0.1.4,20.4.4
#  0  ,  1  ,  2  ,  3  ,  4  ,  5  ,..,  9  ,
#
#gas:   (out%10)%5
#brake: (out%25)/5
#steer: out/25
#10= gerade 0=0%pedal
#5,
#499