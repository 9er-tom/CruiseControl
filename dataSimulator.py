from multiprocessing import Process, Queue
import watchdog

# simulates input for GUI to show

q = Queue()
gui = Process(target=watchdog.App, args=(q,))
gui.start()

counter = 0
while True:
    counter = counter + 1
    q.put((counter, [0]))
    #if counter % 10 == 0:
    #    pass
    #else:
    #    q.put(None)
#