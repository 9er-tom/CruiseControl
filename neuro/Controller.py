from OutputFunctions import steer, usepedals
import time
def control(out): #0-48
    out-=24
    #steeer = (int(out/5)/4)
    #print("Out",out,"Steer",abs((int(out/5)/4)),"Pedal",(int(round((out/5)-int(out/5),1)*5))/4)
    pedals = (int(round((out/5)-int(out/5),1)*5))/4
    steer(abs((int(out/5)/4))/3+(1/3))
    usepedals(brake=pedals*(-1),throttle=pedals)


def hardcontrolnine(out): #0-8
    if(out==0):
        steer(0.3)
        usepedals(throttle=0.5)
    elif(out==1):
        steer()
        usepedals(throttle=0.5)
    elif(out==2):
        steer(0.7)
        usepedals(throttle=0.5)
    elif(out==3):
        steer(0.3)
        usepedals(throttle=0)
    elif(out==4):
        steer()
        usepedals(throttle=0)
    elif(out==5):
        steer(0.7)
        usepedals(throttle=0)
    elif(out==6):
        steer(0.3)
        usepedals(brake=0.7)
    elif(out==7):
        steer()
        usepedals(brake=0.7)
    elif(out==8):
        steer(0.7)
        usepedals(brake=0.7)
    else:
        print("SHIIIIIIIIIIT\n\n")

def hardcontrolfifteen(out):  # 0-14
    if (out == 0):
        steer(0.42)
        usepedals(throttle=0.5)
    elif (out == 1):
        steer(0.47)
        usepedals(throttle=0.5)
    elif (out == 2):
        steer()
        usepedals(throttle=0.5)
    elif (out == 3):
        steer(0.53)
        usepedals(throttle=0.5)
    elif (out == 4):
        steer(0.58)
        usepedals(throttle=0.5)
    elif (out == 5):
        steer(0.42)
        usepedals(throttle=0)
    elif (out == 6):
        steer(0.47)
        usepedals(throttle=0)
    elif (out == 7):
        steer()
        usepedals(throttle=0)
    elif (out == 8):
        steer(0.53)
        usepedals(throttle=0)
    elif (out == 9):
        steer(0.57)
        usepedals(throttle=0)
    elif (out == 10):
        steer(0.42)
        usepedals(brake=0.7)
    elif (out == 11):
        steer(0.47)
        usepedals(brake=0.7)
    elif (out == 12):
        steer()
        usepedals(brake=0.7)
    elif (out == 13):
        steer(0.53)
        usepedals(brake=0.7)
    elif (out == 14):
        steer(0.57)
        usepedals(brake=0.7)
    else:
        print("SHIIIIIIIIIIT\n\n")

    #steer((int(out/25))/20)
    #print((out%25)/5)
    #print(((out%10)%5)/5)
    #usepedals(throttle=((out%10)%5)/5,brake=(out%25)/5)

#0.0.0,0.0.1,0.0.3,0.0.3,0.0.4,0.1.0,..,0.1.4,20.4.4
#  0  ,  1  ,  2  ,  3  ,  4  ,  5  ,..,  9  ,
#
#gas:   (out%10)%5
#brake: (out%25)/5
#steer: out/25
#10= gerade 0=0%pedal
#5,
#499