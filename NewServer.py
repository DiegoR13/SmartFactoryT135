#!/bin/python

from pyModbusTCP.client import ModbusClient
from time import sleep

class Server():
    def __init__(self):
        self.reg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.server = ModbusClient(host="10.22.183.69", port=12345)
        self.EstadosRobot = ["Reset","Charging","EnCaminoaModula","RecogiendoEnModula",
        "EnCaminoaConveyorA","DejandoEnConveyorA","EnCaminoaABBM","DejandoEnABBM",
        "Libre","EnCaminoaHOME","EnCaminoaConveyorC","RecogiendoEnConveyorC",
        "EnCaminoaABBP","DejandoEnABBP","EnCaminoaABBT","RecogiendoEnABBT",
        "EnCaminoaAlmacen","DejandoEnAlamcen"]
        self.EstadosMision = ["PENDING","ACTIVE","PREEMPTED","SUCCEEDED",
        "ABORTED","REJECTED","PREEMPTING","RECALLING","RECALLED","LOST"]
    
    def Vars(self):
        if self.server.open():
            self.reg = self.server.read_holding_registers(0,19)
        self.PzasMod = self.reg[1]
        self.StatConv = self.reg[2]
        self.StatABB = self.reg[3]
        self.PzasAlm = self.reg[4]
        self.RSx1 = self.reg[5]
        self.MSx1 = self.reg[6]
        self.Batx1 = self.reg[7]
        self.GXx1 = self.reg[8]
        self.GYx1 = self.reg[9]
        self.CXx1 = self.reg[10]
        self.CYx1 = self.reg[11]

        self.RSx2 = self.reg[12]
        self.MSx2 = self.reg[13]
        self.Batx2 = self.reg[14]
        self.GXx2 = self.reg[15]
        self.GYx2 = self.reg[16]
        self.CXx2 = self.reg[17]
        self.CYx2 = self.reg[18]
        
        # self.RSOM = self.reg[21]
        # self.MSOM = self.reg[22]
        # self.BatOM = self.reg[23]
        # self.GXOM = self.reg[24]
        # self.GYOM = self.reg[25]
        # self.CXOM = self.reg[26]
        # self.CYOM = self.reg[27]
        
        self.VarsTransf()


    def VarsTransf(self):
        if self.reg[0] == 0:
            self.statusCol = "#e80000"
            self.statusTxt = "Detenido"
        elif self.reg[0] == 1:
            self.statusCol = "#f58700"
            self.statusTxt = "En Reposo"
        elif self.reg[0] == 2:
            self.statusCol = "#31c414"
            self.statusTxt = "En Operacion"
        elif self.reg[0] == 3:
            self.statusCol = "#06c0d1"
            self.statusTxt = "Terminado"

        # Texto Estados Robot
        self.RSx1 = self.EstadosRobot[self.reg[5]]
        self.RSx2 = self.EstadosRobot[self.reg[12]]
        # self.RSOM = self.EstadosRobot[self.reg[21]]
        #Texto Estados Mision
        self.MSx1 = self.EstadosMision[self.reg[6]]
        self.MSx2 = self.EstadosMision[self.reg[13]]
        # self.MSOM = self.EstadosMision[self.reg[22]]
            
        if (self.reg[7] >= 0) and (self.reg[7]<25):
            self.Batx1Col = "#d40404"
        elif (self.reg[7] >= 25) and (self.reg[7]<50):
            self.Batx1Col = "#c47206"
        elif (self.reg[7] >= 50) and (self.reg[7]<75):
            self.Batx1Col = "#fae20c"
        elif (self.reg[7] >= 75) and (self.reg[7]<=100):
            self.Batx1Col = "#02db0d"

        if (self.reg[14] >= 0) and (self.reg[14]<25):
            self.Batx2Col = "#d40404"
        elif (self.reg[14] >= 25) and (self.reg[14]<50):
            self.Batx2Col = "#c47206"
        elif (self.reg[14] >= 50) and (self.reg[14]<75):
            self.Batx2Col = "#fae20c"
        elif (self.reg[14] >= 75) and (self.reg[14]<=100):
            self.Batx2Col = "#02db0d"

        # if (self.reg[23] >= 0) and (self.reg[23]<25):
        #     self.BatOmCol = "#d40404"
        # elif (self.reg[23] >= 25) and (self.reg[23]<50):
        #     self.BatOmCol = "#c47206"
        # elif (self.reg[23] >= 50) and (self.reg[23]<75):
        #     self.BatOmCol = "#fae20c"
        # elif (self.reg[23] >= 75) and (self.reg[23]<=100):
        #     self.BatOmCol = "#02db0d"

        self.xBatx1 = self.reg[7]*1.5
        self.xBatx2 = self.reg[14]*1.5
        # self.xBatOM = self.reg[23]*1.5

        firstx1 = int(self.CXx1/10000)
        if firstx1 == 1:
            self.CXx1 = (self.CXx1-firstx1*10000)/1000
        else:
            self.CXx1 = (-(self.CXx1-firstx1*10000))/1000

        firsty1 = int(self.CYx1/10000)
        if firsty1 == 1:
            self.CYx1 = (self.CYx1-firsty1*10000)/1000
        else:
            self.CYx1 = (-(self.CYx1-firsty1*10000))/1000

        firstx2 = int(self.CXx2/10000)
        if firstx2 == 1:
            self.CXx2 = (self.CXx2-firstx2*10000)/1000
        else:
            self.CXx2 = (-(self.CXx2-firstx2*10000))/1000

        firsty2 = int(self.CYx2/10000)
        if firsty2 == 1:
            self.CYx2 = (self.CYx2-firsty2*10000)/1000
        else:
            self.CYx2 = (-(self.CYx2-firsty2*10000))/1000