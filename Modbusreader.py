#!/bin/python

from pyModbusTCP.client import ModbusClient
from time import sleep
class Server():
    def __init__(self):
        self.hold = [0]
        self.inp = [0]
        self.coil = [0]
        # self.server = ModbusClient("10.22.244.185", 3000)
        # self.server = ModbusClient("10.22.240.51", 2022)
        self.server = ModbusClient("10.22.247.213", 1502)
    
    def getData(self):
        try:
            self.hold = self.server.read_holding_registers(0,19)
            # self.inp = self.server.read_input_registers(0,10)
            # self.coil = self.server.read_coils(0,10)
            print(self.hold)
            # print(self.inp)
            # print(self.coil)
            sleep(1)

        except Exception:
            print("Server is offline")
            print(Exception)

sr = Server()
x=0
while x<100:
    sr.getData()
    x+=1