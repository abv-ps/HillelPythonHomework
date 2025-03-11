import threading
import time

#lock = threading.Semaphore(2) # Контрольований вхід, контрольований вихід з обмеженням потоків (2шт.)
lock = threading.BoundedSemaphore(2) # Контрольований вхід, неконтрольований вихід, не можна release більше, ніж взяли

def worker(number):
    with lock:
        print(f"worker {number} thread is running")
        time.sleep(2)
        print(f"worker {number} thread is stopped")


thread1 = threading.Thread(target=worker, args=(20,))
thread2 = threading.Thread(target=worker, args=(7,))
thread1.start()
thread2.start()
thread1.join()
thread2.join()

