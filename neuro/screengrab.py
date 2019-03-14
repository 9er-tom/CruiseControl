from __future__ import division

import numpy as np
from PIL import ImageGrab as grab
import cv2
import InputFunctions
np.set_printoptions(threshold=np.nan)

killme = True
ostepearlier = None
istepearlier = None
iistepearlier = None
iiistepearlier = None
#otimeearlier = InputFunctions.get_game_time()
#itimeearlier = None
#iitimeearlier = None
#iiitimeearlier = None
#lap0time=0
# def process_image(original_image):

def reset():
    global killme
    global ostepearlier
    global istepearlier
    global iistepearlier
    global iiistepearlier
    #global otimeearlier
    #global itimeearlier
    #global iitimeearlier
    #global iiitimeearlier
    #global lap0time

    killme = True
    ostepearlier = None
    istepearlier = None
    iistepearlier = None
    iiistepearlier = None
    otimeearlier = InputFunctions.get_game_time()
    itimeearlier = None
    iitimeearlier = None
    iiitimeearlier = None
    lap0time = 0

def process_image(og_image):
    thresh = 80
    # proc_screen = cv2.cvtColor(og_image, cv2.COLOR_BGR2GRAY)
    # proc_screen = cv2.threshold(proc_screen, 90, 255, cv2.THRESH_BINARY)[1]
    proc_screen = np.array(og_image.convert('L'))
    proc_screen = cv2.resize(proc_screen, (40, 40))
    proc_screen[proc_screen < thresh] = 0
    proc_screen[proc_screen >= thresh] = 255
    input_array = np.ndarray.flatten(proc_screen)
    input_array[input_array == 255] = 1
    cv2.imshow('map cap', proc_screen)
    return input_array

def process_imagews(og_image):
    global killme
    global ostepearlier
    global istepearlier
    global iistepearlier
    global iiistepearlier
    #global otimeearlier
    #global itimeearlier
    #global iitimeearlier
    #global iiitimeearlier
    #global lap0time
    thresh = 80
    # proc_screen = cv2.cvtColor(og_image, cv2.COLOR_BGR2GRAY)
    # proc_screen = cv2.threshold(proc_screen, 90, 255, cv2.THRESH_BINARY)[1]
    proc_screen = np.array(og_image.convert('L'))
    proc_screen = cv2.resize(proc_screen, (40, 40))
    proc_screen[proc_screen < thresh] = 0
    proc_screen[proc_screen >= thresh] = 255
    input_array = np.ndarray.flatten(proc_screen)
    input_array = np.array(input_array, dtype=float)
    input_array[input_array == 255.] = 1.
    #print(input_array)

    if iistepearlier is not None:
        #iiitimeearlier = iitimeearlier
        #iitimeearlier = itimeearlier
        #itimeearlier = otimeearlier
        #if otimeearlier>InputFunctions.get_game_time() and lap0time == 0:
        #    lap0time = otimeearlier
        #otimeearlier = InputFunctions.get_game_time()
        iiistepearlier = np.multiply(iistepearlier,0.5)#(iitimeearlier/iiitimeearlier))
    if istepearlier is not None:
        #if iistepearlier is None:
        #    iitimeearlier = itimeearlier
        #    itimeearlier = otimeearlier
        iistepearlier = np.multiply(istepearlier,0.5)#(itimeearlier/iitimeearlier))
    if ostepearlier is not None:
        #if istepearlier is None:
        #    itimeearlier = otimeearlier
        #    otimeearlier = InputFunctions.get_game_time()
        istepearlier = np.multiply(ostepearlier,0.5)#(otimeearlier / itimeearlier))
        #print(istepearlier)
    ostepearlier = np.copy(input_array)
    #input_array = np.add(ostepearlier,istepearlier,iistepearlier)

    if istepearlier is not None:
        i = 0
        while i < len(istepearlier):
            if (input_array[i] < istepearlier[i]):
                input_array[i] = istepearlier[i]
            i += 1

    if iistepearlier is not None:
        i = 0
        while i < len(iistepearlier):
            if (input_array[i] < iistepearlier[i]):
                input_array[i] = iistepearlier[i]
            i += 1
    if iiistepearlier is not None:
        i = 0
        while i < len(iiistepearlier):
            if (input_array[i] < iiistepearlier[i]):
                input_array[i] = iiistepearlier[i]
                #print(input_array[i], " ist jetzt ", iiistepearlier[i])
            i += 1
        if killme:
            np.savetxt("plzno.txt", input_array)
            killme = False
    #print(input_array)
    #cv2.imshow('map cap', proc_screen)
    #print(input_array)
    return input_array


def grab_screen():
        screen = grab.grab(bbox=(70, 400, 230, 520))  # AC 800x600, upper left corner of screen
        # screen = np.array(grab.grab(bbox=(700, 450, 900, 750)))
        # screen = np.array(grab.grab(bbox=(300, 480, 500, 780)))
        retval = process_imagews(screen)
        #retval = process_image(screen)
        return retval


if __name__ == '__main__':
    while True:
        grab_screen()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break