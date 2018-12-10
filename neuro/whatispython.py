from PIL import Image
import cv2
import numpy as np
from neuro.Controller import control
import time
from decimal import Decimal
import InputFunctions
import neuro.screengrab as screengrab
import os
import sys
import platform
import numpy
from sim_info import info
import time

while True:
    print(InputFunctions.isinbox())

'''
col = Image.open("Aertong.png")
gray = col.convert('L')

# Let numpy do the heavy lifting for converting pixels to pure black or white
bw = np.asarray(gray).copy()
bw = cv2.resize(bw, dsize=(40, 40), interpolation=cv2.INTER_CUBIC)
# Pixel range is 0...255, 256/2 = 128
bw[bw < 70] = 0    # Black
bw[bw >= 184] = 255 # White set to 1

print(bw)

# Now we put it back in Pillow/PIL land
imfile = Image.fromarray(bw)
imfile.save("result_bw.png")




time.sleep(5)
i=0
while i<49:
    control(i)
    i+=1
    time.sleep(0.5)
'''

#state = InputFunctions.get_info()
#state=np.append(state,screengrab.grab_screen())
#print(stat# e)



'''
cnt_enabled = False  # countdown
flyingstart = 1
timewaiting = 0

if platform.architecture()[0] == "64bit":
    sysdir = "stdlib64"
else:
    sysdir = "stdlib"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "my_super_app_lib", sysdir))
os.environ['PATH'] = os.environ['PATH'] + ";."


while True:
    print(info.graphics.iCurrentTime)
'''
