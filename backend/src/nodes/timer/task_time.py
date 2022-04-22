import threading
from bson.objectid import ObjectId

def setInterval(interval, stop_event=None, name=""):
    """
    Decorator to set a function to be called at every interval seconds.

    Usage:
        @setInterval(n)\n
        def my_function():
            print("Hello")
        
        stop_event_setter = my_function() 

    - start the function, and get the returned stop event
    - After 'n' seconds, the function will be called again.
    - Use stop_event_setter.set() to stop the function.

    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event() if stop_event is None else stop_event

            def loop():
                while not stopped.wait(interval): 
                    function(*args, **kwargs)

            t = threading.Thread(name=f"{name}_{ObjectId()}", target=loop)
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