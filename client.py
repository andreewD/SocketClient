import threading
import socketio
import numpy as np
import time
# standard Python
sio = socketio.Client()

sio.connect('https://socket-server-cc.herokuapp.com/')


def fun1(x, y, n):
    global x_y
    x_y = 0
    for i in range(n):
        x_y = x_y + x[i]*y[i]
    return x_y


def fun2(x, y, n):
    global sum_x
    sum_x = 0
    for i in range(n):
        sum_x = sum_x + x[i]
    return sum_x


def fun3(x, y, n):
    global sum_y
    sum_y = 0
    for i in range(n):
        sum_y = sum_y + y[i]
    return sum_y


def fun4(x, y, n):
    global x_x
    x_x = 0
    for i in range(n):
        x_x = x_x + x[i]*x[i]
    return x_x


def main(tarea, x, y):
    # global x_y, sum_x, sum_y, x_x
    # sum_x = 0
    # sum_y = 0
    # x_x = 0
    # x_y = 0

    n = len(x)
    n1 = len(x)
    n2 = len(y)
    print(n1, n2)

    t1 = threading.Thread(name="hilo_1", target=fun1, args=(x, y, n))
    t2 = threading.Thread(name="hilo_2", target=fun2, args=(x, y, n))
    t3 = threading.Thread(name="hilo_1", target=fun3, args=(x, y, n))
    t4 = threading.Thread(name="hilo_2", target=fun4, args=(x, y, n))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    print(x_y, sum_x, sum_y, x_x)

    a = (n*x_y - sum_x*sum_y)/(n*x_x - sum_x*sum_x)

    b = (sum_y - a*sum_x)/n

    print(a, b)


@sio.event
def message(data):
    a = data[0]
    tarea, x, y = a['index'], a['X'], a['Y']
    print(tarea)
    print(x)
    print(y)
    main(tarea, x, y)
