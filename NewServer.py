#!/bin/python

from pyModbusTCP.client import ModbusClient
from time import sleep
import math

class Server():
    def __init__(self):
        self.reg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.regOmron = [0,0,0,0,0,0]
        self.server = ModbusClient(host="10.22.240.51", port=2022)
        self.OMRON = ModbusClient(host="10.22.247.213", port=1502)
        # self.server = ModbusClient(host="192.168.100.10", port=12345) ##Para Simulaciones
        # self.OMRON = ModbusClient(host="192.168.100.10", port=2000) #Para Simulaciones
        self.EstadosRobot = ["Reset","Charging","En Camino a Modula","Recogiendo En Modula",
        "En Camino a Conveyor1","Dejando En Conveyor1","Libre","En Camino a HOME",
        "En Camino a Conveyor2","Recogiendo en Conveyor2","En Camino a ABB Place","Dejando en ABB Place",
        "En Camino a ABB Pick","Recogiendo en ABB Pick", "En Camino a Almacen","Dejando En Alamcen","Desactivado","En Espera"]
        self.EstadosMision = ["PENDING","ACTIVE","PREEMPTED","SUCCEEDED",
        "ABORTED","REJECTED","PREEMPTING","RECALLING","RECALLED","LOST"]
        self.EstadosModula = ["Vacio", "Piezas Disponibles"]
        self.EstadosAlmacen = ["Vacio", "Lleno"]
    
    def Vars(self):
        if self.server.open():
            self.reg = self.server.read_holding_registers(0,21)
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

        if self.OMRON.open():
            self.regOmron = self.OMRON.read_holding_registers(5,5)
        self.RSOM = self.regOmron[0]

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
        self.RSOM = self.EstadosRobot[self.regOmron[0]]
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

        
        #Transformar datos de current pos Smart1
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

        #Transformar datos de goal Smart1
        firstgx1 = int(self.GXx1/10000)
        if firstgx1 == 1:
            self.GXx1 = (self.GXx1-firstgx1*10000)/1000
        else:
            self.GXx1 = (-(self.GXx1-firstgx1*10000))/1000

        firstgy1 = int(self.GYx1/10000)
        if firstgy1 == 1:
            self.GYx1 = (self.GYx1-firstgy1*10000)/1000
        else:
            self.GYx1 = (-(self.GYx1-firstgy1*10000))/1000

        #Transformar datos de current pos Smart2
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

        #Transformar datos de Goal Smart2
        firstgx2 = int(self.GXx2/10000)
        if firstgx2 == 1:
            self.GXx2 = (self.GXx2-firstgx2*10000)/1000
        else:
            self.GXx2 = (-(self.GXx2-firstgx2*10000))/1000

        firstgy2 = int(self.GYx2/10000)
        if firstgy2 == 1:
            self.GYx2 = (self.GYx2-firstgy2*10000)/1000
        else:
            self.GYx2 = (-(self.GYx2-firstgy2*10000))/1000

        self.distSMART1 = math.sqrt(((self.GXx1-self.CXx1)**2) + ((self.GYx1-self.CYx1)**2))
        self.distSMART2 = math.sqrt(((self.GXx2-self.CXx2)**2) + ((self.GYx2-self.CYx2)**2))

        if self.PzasMod == 0:
            self.PzasMod = self.EstadosModula[0]
        elif self.PzasMod == 1:
            self.PzasMod = self.EstadosModula[1]

        if self.PzasAlm == 0:
            self.PzasAlm = self.EstadosAlmacen[0]
        elif self.PzasAlm == 1:
            self.PzasAlm = self.EstadosAlmacen[1]

        if (self.reg[5] == 1) or (self.reg[5] == 6):
            self.colorx1 = "#000000"
        else:
            self.colorx1 = "#f78902"

        if (self.reg[12] == 1) or (self.reg[12] == 6):
            self.colorx2 = "#000000"
        else:
            self.colorx2 = "#f78902"

    def changeStates(self,state,value):
        self.server.write_single_register(state,value)
