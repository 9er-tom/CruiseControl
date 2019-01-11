import tkinter as tk
import psutil
from InputFunctions import get_car_info, get_lap_info


def counter_label(textlabel):
    def count():
        textlabel.config(text=str(get_car_info()[3]))
        textlabel.after(1, count)

    count()


root = tk.Tk()
root.title("CruiseControl Info")
label = tk.Label(root)
label.pack()
counter_label(label)
root.mainloop()
