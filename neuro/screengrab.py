import numpy as np
from PIL import ImageGrab as grab
import cv2


# def process_image(original_image):

def process_image(og_image):
    thresh = 80
    # proc_screen = cv2.cvtColor(og_image, cv2.COLOR_BGR2GRAY)
    # proc_screen = cv2.threshold(proc_screen, 90, 255, cv2.THRESH_BINARY)[1]
    proc_screen = np.array(og_image.convert('L'))
    proc_screen[proc_screen < thresh] = 0
    proc_screen[proc_screen >= thresh] = 255
    proc_screen = cv2.resize(proc_screen, (40, 40))
    input_array = np.ndarray.flatten(proc_screen)
    input_array[input_array == 255] = 1
    return input_array


def grab_screen():
        screen = grab.grab(bbox=(50, 600 - 210, 250, 600))  # AC 800x600, upper left corner of screen
        # screen = np.array(grab.grab(bbox=(700, 450, 900, 750)))
        # screen = np.array(grab.grab(bbox=(300, 480, 500, 780)))
        return process_image(screen)
        # return retval


if __name__ == '__main__':
    while True:
        grab_screen()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
