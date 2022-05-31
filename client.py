import socketio
import threading
import json

# standard Python
sio = socketio.Client()


@sio.event
def connect():
    print("Connect")


@sio.event
def connect_error(data):
    print('Connect error')


@sio.event
def disconnect():
    print('Disconnect')


@sio.event
def message(data):
    print('Datos receividos')
    main(data)


sio.connect('https://socket-server-cc.herokuapp.com/')


def main(data):
    result = list()
    print("Empezando...")
    for line in data:
        tes = work(line)
        result.append(tes)
    print("Finalizado...")
    print(json.dumps(result, sort_keys=True, indent=4))
    # sio.send(result)


def work(data):
    index = int(data["index"])
    x = list(data["X"])
    y = list(data["Y"])
    n = int(len(x))

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

    status = 'Success'
    result = {'index': index, 'status': status, 'SX': sum_x,
              'SY': sum_y, 'SXX': x_x, 'SXY': x_y, 'SN': n}
    return result


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
