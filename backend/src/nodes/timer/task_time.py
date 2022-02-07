import threading

def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():
                while not stopped.wait(interval): 
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True 
            t.start()
            return stopped
        return wrapper
    return decorator

if __name__ == '__main__':
    from time import sleep
    @setInterval(1)
    def print_time():
        print(threading.currentThread().getName(), "say: Hello, world!")
    print_time()
    for n in range(5):
        sleep(1)