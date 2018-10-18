import numpy as np
from PIL import ImageGrab as grab
import cv2


# def process_image(original_image):

def process_image(og_image):

    proc_screen = cv2.cvtColor(og_image, cv2.COLOR_BGR2GRAY)
    proc_screen = cv2.threshold(proc_screen, 90, 255, cv2.THRESH_BINARY)[1]
    # proc_screen = cv2.Canny(og_image, threshold1=200, threshold2=300)

    cv2.imshow('map cap', proc_screen)


if __name__ == '__main__':
    while True:
        screen = np.array(grab.grab(bbox=(700, 480, 900, 780)))
        # screen = np.array(grab.grab(bbox=(300, 480, 500, 780)))
        process_image(screen)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        break