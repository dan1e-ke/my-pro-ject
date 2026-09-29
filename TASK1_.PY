
# TASK 1:
# Increase buffer size to 10
import threading
import time
import random
from queue import Queue
from threading import Semaphore

BUFFER_SIZE = 10

# Shared buffer
buffer = Queue(BUFFER_SIZE)

# Semaphores
empty = Semaphore(BUFFER_SIZE)
full = Semaphore(0)
mutex = Semaphore(1)


# Producer function
def producer(pid):
    while True:
        item = random.randint(1, 100)

        time.sleep(random.uniform(0.5, 1.5))

        print(f"Producer {pid} waiting for empty slot...")

        empty.acquire()
        mutex.acquire()

        buffer.put(item)

        print(
            f"Producer {pid} produced {item} | "
            f"Buffer size: {buffer.qsize()}"
        )

        mutex.release()
        full.release()


# Consumer function
def consumer(cid):
    while True:
        full.acquire()
        mutex.acquire()

        item = buffer.get()

        print(
            f"Consumer {cid} consumed {item} | "
            f"Buffer size: {buffer.qsize()}"
        )

        mutex.release()
        empty.release()

        time.sleep(random.uniform(1, 2))


# Threads
producers = [
    threading.Thread(target=producer, args=(0,))
]

consumers = [
    threading.Thread(target=consumer, args=(0,))
]

for t in producers + consumers:
    t.daemon = True
    t.start()

time.sleep(10)

print("Task 1 simulation complete.")
# Observation:
# Producers are blocked less often.
# More items can wait in the buffer.
#System throughput improves compared to buffer size 5.
