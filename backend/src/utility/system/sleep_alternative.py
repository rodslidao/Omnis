from timeit import default_timer as timer

def sleep(secs):
    T0 = timer()
    while timer() - T0 < secs:
        pass