from PIL import Image
import cv2
import numpy as np

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


#from neuro.Controller import control
#import time

#i=0
#while i<500:
#    control(i)
#    i+=1
#    time.sleep(0.02)