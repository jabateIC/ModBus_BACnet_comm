# - * - coding: utf - 8 -
# *-
"""
Created on Fri Oct 22 12:27:19 2021
@author: IvanChan
"""
import numpy as np
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import numpy
import time


def get():
    return np.random.randint(100)


p = {'name': 'Woof', 'addr': 1, 'get': get}
server = modbus_tcp.TcpServer(address='127.0.0.1', port=5020)
slave1 = server.add_slave(1)
param = []
param.append(p)


def main():
    for p in param:
        slave1.add_block(p['name'], cst.HOLDING_REGISTERS, p['addr'], 1)
        server.start()
    try:
        while True:
            for p in param:
                x = p['get']()
                print(x)
                slave1.set_values(p['name'], p['addr'], x)

            time.sleep(1)
    finally:
        server.stop()


if __name__ == "__main__":
    main()
