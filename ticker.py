import threading


def f(f_stop):

    # do something here ...

    if not f_stop.is_set():

        # call f() again in 60 seconds

        threading.Timer(60, f, [f_stop]).start()


f_stop = threading.Event()

# start calling f now and every 60 sec thereafter

f(f_stop)


# stop the thread when needed

#f_stop.set()
