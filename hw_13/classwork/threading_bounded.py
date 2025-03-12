import threading
import time

lock = threading.Semaphore(2)

def worker(number):
    print(f"Thread {number} thread is waiting...")
    lock.acquire()
    print(f"Thread {number} thread is started...")
    time.sleep(2)
    lock.release()
    print(f"Thread {number} thread is stopped")


thread1 = threading.Thread(target=worker, args=(20,))
thread2 = threading.Thread(target=worker, args=(10,))
thread3 = threading.Thread(target=worker, args=(15,))
thread4 = threading.Thread(target=worker, args=(7,))
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()


"""
Semaphore
Thread 20 thread is waiting...
Thread 20 thread is started...
Thread 10 thread is waiting...
Thread 10 thread is started...
Thread 15 thread is waiting...
Thread 7 thread is waiting...
Thread 20 thread is stoppedThread 10 thread is stoppedThread 15 thread is started...


Thread 7 thread is started...
Thread 15 thread is stopped
Thread 7 thread is stopped"""