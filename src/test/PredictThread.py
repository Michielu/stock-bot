import threading
import time

exitFlag = 0


class PredictThread1 (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, 5, self.counter)
        print("Exiting " + self.name)
        return "helo"


def print_time(threadName, counter, delay):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


# Create new threads
thread1 = PredictThread1(1, "Thread-1", 1)
thread2 = PredictThread1(2, "Thread-2", 2)

# Start new Threads
a = thread1.start()
b = thread2.start()
print("a and b are: ", a, b)
print("Exiting Main Thread")
