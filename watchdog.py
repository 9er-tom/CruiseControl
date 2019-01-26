import tkinter as tk
from tkinter import ttk
import psutil as ps
from InputFunctions import get_car_position
from multiprocessing import Queue


# Source: https://www.raspberrypi.org/forums/viewtopic.php?t=188251

class Mainframe(tk.Frame):
    # Mainframe contains the widgets
    def __init__(self, master, conn):
        tk.Frame.__init__(self, master)

        self.TimerInterval = 500  # in milliseconds

        # multiprocessing queue
        self.conn = conn
        self.cr, self.ra = 1, [0]  # initialising current reward and reward array fixme: shit's not saving, yo
        # self.prev_RA, self.prev_CR = [0], 0  # previous reward array and current reward, initialised with 0

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

        # separator
        ttk.Separator(self, orient="horizontal").grid(row=2, columnspan=100, sticky="we")

        # current track progress
        self.track_progress = tk.DoubleVar()
        tk.Label(self, text="Track progress").grid(row=3, sticky="w")
        tk.Label(self, text=" - ").grid(row=3, column=1)
        tk.Label(self, textvariable=self.track_progress).grid(row=3, column=2)
        tk.Label(self, text="%").grid(row=3, column=3)

        # cumulative reward
        self.current_cumulative_reward = tk.DoubleVar()
        tk.Label(self, text="Cumulative reward").grid(row=4, sticky="w")
        tk.Label(self, text=" - ").grid(row=4, column=1)
        tk.Label(self, textvariable=self.current_cumulative_reward).grid(row=4, column=2)

        # total average reward
        self.total_average_reward = tk.DoubleVar()
        tk.Label(self, text="Total average reward").grid(row=5, sticky="w")
        tk.Label(self, text=" - ").grid(row=5, column=1)
        tk.Label(self, textvariable=self.total_average_reward).grid(row=5, column=2)

        self.update_labels()

    def update_labels(self):
        queue_content = self.conn.get()
        if queue_content is not None:
            self.cr, self.ra = queue_content
            # self.prev_CR, self.prev_RA = cumulative_reward, reward_array
        # else:
        #   cumulative_reward, reward_array = self.prev_CR, self.prev_RA

        self.cpu_usage.set(ps.cpu_percent())
        self.used_ram.set(round(ps.virtual_memory().used / 10 ** 9, 2))
        self.max_ram.set(round(ps.virtual_memory().available / 10 ** 9, 2))

        self.track_progress.set(round(get_car_position() * 100, 4))

        self.total_average_reward.set(sum(self.ra) / len(self.ra))
        self.current_cumulative_reward.set(self.cr)

        # repeat call
        self.after(self.TimerInterval, self.update_labels)


class App(tk.Tk):
    def __init__(self, conn):
        tk.Tk.__init__(self)
        # set the title bar text
        self.title('CruiseControl WatchDog')
        # Make sure app window is big enough to show title
        self.geometry('300x200')

        # create and pack a Mainframe window
        Mainframe(self, conn).pack()

        # now start
        self.mainloop()


# create an App object
# it will run itself
if __name__ == '__main__':
    q = Queue()
    q.put((0, [1, 2, 3]))
    App(q)
