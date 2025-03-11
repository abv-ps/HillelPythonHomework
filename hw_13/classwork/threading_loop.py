import  threading

def print_numbers():
    total = 1
    for i in range(100):
        total *= 1*2
    print(total)



thread_1 = threading.Thread(target=print_numbers)
thread_2 = threading.Thread(target=print_numbers)
thread_3 = threading.Thread(target=print_numbers)
thread_4 = threading.Thread(target=print_numbers)
thread_5 = threading.Thread(target=print_numbers)
thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()
thread_5.start()
thread_1.join()
thread_2.join()
thread_3.join()
thread_4.join()
thread_5.join()
