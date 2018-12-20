import tkinter as tk
import psutil


def counter_label(textlabel):
    def count():
        textlabel.config(text=str(psutil.disk_io_counters()))
        textlabel.after(1, count)

    count()


root = tk.Tk()
root.title("Counting Seconds")
label = tk.Label(root, fg="green")
label.pack()
counter_label(label)
root.mainloop()
