# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 12:10:17 2021
@author: IvanChan
"""
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import struct
import threading


def f(f_stop):
    masterTCP = modbus_tcp.TcpMaster(host='127.0.0.1', port=5020)
    # masterTCP = modbus_tcp.TcpMaster(host='192.168.127.252', port=502)
    masterTCP.set_timeout(1)
    masterTCP.set_verbose(True)
    # %%
    ret = masterTCP.execute(
        slave=1,
        function_code=cst.HOLDING_REGISTERS,
        starting_address=1,
        quantity_of_x=1)
    print(ret)
    if not f_stop.is_set():
        # call f() again in 3 seconds
        threading.Timer(1, f, [f_stop]).start()


f_stop = threading.Event()
# start calling f now and every 3 sec thereafter
f(f_stop)


def main():
    f(f_stop)


if __name__ == "__main__":
    main()
