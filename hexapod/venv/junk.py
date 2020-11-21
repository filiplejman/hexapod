import time


def calculate_time(func):
    def inner(*args, **kwargs):
        begin = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("Total time taken in : ", func.__name__, end - begin)
    return inner


@calculate_time
def loop(times):
    for _ in range(times):
        time.sleep(0.1)
    print("ending")


@calculate_time
def add(x, y):
    print(x+y)


add(19, 5)
loop(10)
