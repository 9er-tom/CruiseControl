import tkinter as tk
from tkinter import ttk
import psutil as ps
from InputFunctions import get_car_position


# Source: https://www.raspberrypi.org/forums/viewtopic.php?t=188251

class Mainframe(tk.Frame):
    # Mainframe contains the widgets
    # More advanced programs may have multiple frames
    # or possibly a grid of subframes

    def __init__(self, master, *args, **kwargs):
        # *args packs positional arguments into tuple args
        # **kwargs packs keyword arguments into dict kwargs

        # initialise base class
        tk.Frame.__init__(self, master, *args, **kwargs)
        # in this case the * an ** operators unpack the parameters

        # cpu usage in percent
        self.cpu_usage = tk.IntVar()
        tk.Label(self, text="CPU usage").grid(row=0, column=0, sticky='w')
        tk.Label(self, text=" - ").grid(row=0, column=1)
        tk.Label(self, textvariable=self.cpu_usage).grid(row=0, column=2)
        tk.Label(self, text="%").grid(row=0, column=3)

        # used ram/max ram
        self.used_ram = tk.DoubleVar()
        self.max_ram = tk.DoubleVar()
        tk.Label(self, text="free/max RAM").grid(row=1, column=0, sticky='w')
        tk.Label(self, text=" - ").grid(row=1, column=1)
        tk.Label(self, textvariable=self.used_ram).grid(row=1, column=2)
        tk.Label(self, text=" / ").grid(row=1, column=3)
        tk.Label(self, textvariable=self.max_ram).grid(row=1, column=4)
        tk.Label(self, text="GB").grid(row=1, column=5, sticky='w')
        self.TimerInterval = 500  # in milliseconds

        # separator
        ttk.Separator(self, orient="horizontal").grid(row=2, columnspan=100, sticky="we")

        # current track progress
        self.track_progress = tk.DoubleVar()
        tk.Label(self, text="Track progress").grid(row=3, sticky="w")
        tk.Label(self, text=" - ").grid(row=3, column=1)
        tk.Label(self, textvariable=self.track_progress).grid(row=3, column=2)
        tk.Label(self, text="%").grid(row=3, column=3)

        # call Get Temp which will call itself after a delay
        self.update_labels()

    def update_labels(self):
        self.cpu_usage.set(ps.cpu_percent())
        self.used_ram.set(round(ps.virtual_memory().used / 10 ** 9, 2))
        self.max_ram.set(round(ps.virtual_memory().available / 10 ** 9, 2))
        self.track_progress.set(round(get_car_position()*100, 4))
        # repeat call
        self.after(self.TimerInterval, self.update_labels)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # set the title bar text
        self.title('CruiseControl WatchDog')
        # Make sure app window is big enough to show title
        self.geometry('300x100')

        # create and pack a Mainframe window
        Mainframe(self).pack()

        # now start
        self.mainloop()


# create an App object
# it will run itself
# App()
