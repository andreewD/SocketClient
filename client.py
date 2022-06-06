import socketio
import threading
import json
import time
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


@sio.on('calc')
def on_message(data):
    main(data)

# deploy link
# sio.connect('https://socket-server-cc.herokuapp.com/')

# local link
sio.connect('http://localhost:3000')


def main(data):
    result = list()
    timeIni = time.time()
    print("Empezando...")
    for line in data:
        tes = work(line)
        result.append(tes)
    sio.emit('message',json.dumps(result, sort_keys=True, indent=4))
    print("Finalizado...")
    timefin = time.time()
    timeClient = timefin - timeIni
    result.append({"timeClient":timeClient})
    print(json.dumps(result, sort_keys=True, indent=4))
    sio.send(result)
    


def work(data):
    try:
        index = int(data["index"])
        x = list(data["X"])
        y = list(data["Y"])
        n = int(len(x))
        timeIni = time.time()

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

        n = float(len(x))
        formula = convFormula(x_x, x_y,sum_x,sum_y,n)
        timefin = time.time()
        timeWork = timefin - timeIni
    except:
        status = 'Failure'
        result = {'index': index, 'status': status, 'Data':data, 'TimeWork': timeWork}
    finally:
       status = 'Success'
       result = {'index': index, 'status': status, 'formula': formula, 'TimeWork': timeWork}
       return result


def convFormula(x_x, x_y,sum_x,sum_y,n):
    arr01 = n * x_y + sum_x * sum_y
    arr02 = n * x_x - sum_x * sum_x
    a = arr01 / arr02
    b = sum_y - a * sum_x / n
    a = float("{:.2f}".format(a))
    b = float("{:.2f}".format(b))
    formula = 'y = '+str(a)+'x + '+str(b)
    return formula

def fun1(x, y, n):
    global x_y
    x_y = float(0)
    for i in range(n):
        x_y = x_y + float(x[i]*y[i])
    return x_y


def fun2(x, y, n):
    global sum_x
    sum_x = float(0)
    for i in range(n):
        sum_x = sum_x + float(x[i])
    return sum_x


def fun3(x, y, n):
    global sum_y
    sum_y = float(0)
    for i in range(n):
        sum_y = sum_y + float(y[i])
    return sum_y


def fun4(x, y, n):
    global x_x
    x_x = float(0)
    for i in range(n):
        x_x = x_x + float(x[i]*x[i])
    return x_x