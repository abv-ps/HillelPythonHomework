import threading


counter = 0
lock = threading.RLock() # Reverse lock Рекурсивне блокування - декілька разів можна блокувати ті ж самі ресурси
# lock = threading.Lock() # Просте блокування - якщо lock.release() немає, потік не відпускається

def task():
    print(f"Task #{counter}")
    print(f"Start lock")
    lock.acquire()
    print(f"Is locking")
    print(f"Task #{counter+1}")
    #lock.release() для прикладу Rlock
    print(f"Alter lock")
    lock.acquire()
    print(f"Unlock")
    lock.release()
    lock.release()
    # with lock:


threads = [threading.Thread(target=task) for _ in range(2)]

for t in threads:
    t.start()

for t in threads:
    t.join()


print("Counter:", counter)