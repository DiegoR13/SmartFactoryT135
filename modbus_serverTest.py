#!/bin/python

from pyModbusTCP.server import ModbusServer
from time import sleep
# Create an instance of ModbusServer
class Server():
    def __init__(self):
        self.reg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.server = ModbusServer("10.22.183.69", 12345, no_block=True)
    
    def getData(self):
        try:
            print("Start server...")
            self.server.start()
            print("Server is online")
            while True:
                #DataBank.set_words(0, [int(uniform(0, 100))])
                if self.reg != self.server.data_bank.get_holding_registers(0,19):
                    self.reg = self.server.data_bank.get_holding_registers(0,19)
                    print("Value of Registers has changed to " +str(self.reg))
                sleep(0.5)

        except:
            print("Shutdown server ...")
            self.server.stop()
            print("Server is offline")

sr = Server()
sr.getData()