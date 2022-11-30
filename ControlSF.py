from pyModbusTCP.client import ModbusClient
import time
class InfoRegistros:
    EstadoSF = 0
    SeñalModula = 1
    EstadoConv = 2
    EstadoABB = 3
    InfoAlmacen = 4
    EstadoSMART1 = 5
    EstadoMisionSMART1 = 6
    BateriaSMART1 = 7
    GoalXSMART1 = 8
    GoalYSMART1 = 9
    CurrXSMART1 = 10
    CurrYSMART1 = 11
    EstadoSMART2 = 12
    EstadoMisionSMART2 = 13
    BateriaSMART2 = 14
    GoalXSMART2 = 15
    GoalYSMART2 = 16
    CurrXSMART2 = 17
    CurrYSMART2 = 18
    InstruccionPLC = 20
    InstruccionABB = 21

class EstadosROBOT:
    Reset = 0
    Charging = 1
    EnCaminoaModula = 2
    RecogiendoEnModula = 3
    EnCaminoaConveyor1 = 4
    DejandoEnConveyor1 = 5
    Libre = 6
    EnCaminoaHOME = 7
    EnCaminoaConveyor2 = 8
    RecogiendoEnConveyor2 = 9
    EnCaminoaABBPlace = 10
    DejandoEnABBPlace = 11
    EnCaminoaABBPick = 12
    RecogiendoEnABBPick = 13
    EnCaminoaAlmacen = 14
    DejandoEnAlamcen = 15
    Desactivado = 16
    EnEspera = 17

class Modula:
    PedirMaterial = [2,1,1]
    RevisionEstado = [3,1,1]
    ConfirmarOperacion = [4,1,1]

class Control():
    def __init__(self):
        self.server = ModbusClient("10.22.240.51", 2022)
        self.serverModula = ModbusClient("10.22.244.185", 3000)
        self.serverOMRON = ModbusClient("10.22.247.213", 1502)

        # self.server = ModbusClient("192.168.100.10", 12345) #TEST
        # self.serverModula = ModbusClient("192.168.100.10", 2000) #TEST

        self.EstadosSF = {"Detenido":0, "En Reposo": 1, "En Operacion": 2, "Terminado": 3}
        self.registros = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.registroOMRON = [0,0,0,0,0,0]
        self.dir = InfoRegistros()
        self.EstadosROBOT = EstadosROBOT()
        self.instModula = Modula()
        self.operacionModula = False
        self.comprobacionModula = False
        self.materialListo = False
        self.contadorTareasS1 = 0
        self.contadorTareasS2 = 0
        self.estadoSF = 0
        #Info de Tareas y Procesos:
            #Tarea 1: Recoger Fixture de Modula y llevar a conveyor
            #Proceso 1: Prensado en Conveyor con UR
            #Tarea 2: Recoger Fixture prcesado de Conveyor y llevar a ABB
            #Proceso 2: Pegar herrajes en ABB
            #Tarea 3: Recoger Fixture de piezas terminadas y llevarlo a Almacén
        self.Tarea1 = False
        self.Tarea2 = False
        self.Tarea3 = False
        self.Proceso1 = False
        self.Proceso2 = False
        self.robotEnTarea1 = 0
        self.robotEnTarea2 = 0
        self.robotEnTarea3 = 0
        self.memoriaTarea1 = None
        self.memoriaTarea2 = None
        self.memoriaTarea3 = None
        self.verificarFin = False
        self.estadoActivoT1 = None
        self.estadoActivoT2 = None
        self.estadoActivoT3 = None


    def lecturaServidor(self):
        errCon = 0
        if self.server.open():
            errCon = 0
            self.registros = self.server.read_holding_registers(0,21)
            
            self.estadoSF = self.registros[0]
            self.señalModula = self.registros[1]
            self.estadoConveyor = self.registros[2]
            self.estadoABB = self.registros[3]
            self.infoAlmacen = self.registros[4]

            self.SMART1 = {"Estado robot":self.registros[5] , "Estado Mision":self.registros[6] , "Bateria":self.registros[7] ,
            "Goal X":self.registros[8] , "Goal Y":self.registros[9] , "Current X":self.registros[10] , "Current Y":self.registros[11]}
            self.SMART2 = {"Estado robot":self.registros[12] , "Estado Mision":self.registros[13] , "Bateria":self.registros[14] ,
            "Goal X":self.registros[15] , "Goal Y":self.registros[16] , "Current X":self.registros[17] , "Current Y":self.registros[18]}
            
            #Verifica si algun robot está haciendo la Tarea 1
            if (self.SMART1["Estado robot"]==self.EstadosROBOT.EnCaminoaModula or self.SMART1["Estado robot"]==self.EstadosROBOT.RecogiendoEnModula or 
            self.SMART1["Estado robot"]==self.EstadosROBOT.EnCaminoaConveyor1 or self.SMART1["Estado robot"]==self.EstadosROBOT.DejandoEnConveyor1):
                self.robotEnTarea1 = 1
                self.estadoActivoT1 = self.SMART1["Estado robot"]
            elif (self.SMART2["Estado robot"]==self.EstadosROBOT.EnCaminoaModula or self.SMART2["Estado robot"]==self.EstadosROBOT.RecogiendoEnModula or 
            self.SMART2["Estado robot"]==self.EstadosROBOT.EnCaminoaConveyor1 or self.SMART2["Estado robot"]==self.EstadosROBOT.DejandoEnConveyor1):
                self.robotEnTarea1 = 2
                self.estadoActivoT1 = self.SMART2["Estado robot"]
            else:
                self.robotEnTarea1 = 0
                self.estadoActivoT1 = None

            #Verifica si algun robot esta haciendo la Tarea 2
            if (self.SMART1["Estado robot"]==self.EstadosROBOT.EnCaminoaConveyor2 or self.SMART1["Estado robot"]==self.EstadosROBOT.RecogiendoEnConveyor2 or 
            self.SMART1["Estado robot"]==self.EstadosROBOT.EnCaminoaABBPlace or self.SMART1["Estado robot"]==self.EstadosROBOT.DejandoEnABBPlace):
                self.robotEnTarea2 = 1
                self.estadoActivoT2 = self.SMART1["Estado robot"]
            elif (self.SMART2["Estado robot"]==self.EstadosROBOT.EnCaminoaConveyor2 or self.SMART2["Estado robot"]==self.EstadosROBOT.RecogiendoEnConveyor2 or 
            self.SMART2["Estado robot"]==self.EstadosROBOT.EnCaminoaABBPlace or self.SMART2["Estado robot"]==self.EstadosROBOT.DejandoEnABBPlace):
                self.robotEnTarea2 = 2
                self.estadoActivoT2 = self.SMART2["Estado robot"]
            else:
                self.robotEnTarea2 = 0
                self.estadoActivoT2 = None

            #Verifica si algun robot esta haciendo la Tarea 3
            if (self.SMART1["Estado robot"]==self.EstadosROBOT.EnCaminoaABBPick or self.SMART1["Estado robot"]==self.EstadosROBOT.RecogiendoEnABBPick or 
            self.SMART1["Estado robot"]==self.EstadosROBOT.EnCaminoaAlmacen or self.SMART1["Estado robot"]==self.EstadosROBOT.DejandoEnAlamcen):
                self.robotEnTarea3 = 1
                self.estadoActivoT3 = self.SMART1["Estado robot"]
            elif (self.SMART2["Estado robot"]==self.EstadosROBOT.EnCaminoaABBPick or self.SMART2["Estado robot"]==self.EstadosROBOT.RecogiendoEnABBPick or 
            self.SMART2["Estado robot"]==self.EstadosROBOT.EnCaminoaAlmacen or self.SMART2["Estado robot"]==self.EstadosROBOT.DejandoEnAlamcen):
                self.robotEnTarea3 = 2
                self.estadoActivoT3 = self.SMART2["Estado robot"]
            else:
                self.robotEnTarea3 = 0
                self.estadoActivoT3 = None

            #Verifica si algún robot está libre
            if (self.SMART1["Estado robot"] == self.EstadosROBOT.Charging) or (self.SMART1["Estado robot"] == self.EstadosROBOT.Libre): self.SMART1Libre = True
            else: self.SMART1Libre = False
            if (self.SMART2["Estado robot"] == self.EstadosROBOT.Charging) or (self.SMART2["Estado robot"] == self.EstadosROBOT.Libre): self.SMART2Libre = True
            else: self.SMART2Libre = False

        else:
            errCon +=1
            if errCon == 5:
                self.error("No se pudo establecer conexión con el servidor principal",1)

        if self.serverOMRON.open():
            errConOm = 0
            self.registroOMRON = self.serverOMRON.read_holding_registers(5,5)

            self.OMRON = {"Estado robot":self.registroOMRON[0]}

            #Verifica si el OMRON esta libre
            if (self.OMRON["Estado robot"] == self.EstadosROBOT.Charging): self.OMRONLibre = True
            else: self.OMRONLibre = False

            #Verifica si el OMRON esta esperando
            if (self.OMRON["Estado robot"] == self.EstadosROBOT.EnEspera): self.OMRONEsperando = True
            else: self.OMRONEsperando = False

            #Verifica si el OMRON esta haciendo la Tarea 2
            if (self.OMRON["Estado robot"]==self.EstadosROBOT.EnCaminoaConveyor2 or self.OMRON["Estado robot"]==self.EstadosROBOT.RecogiendoEnConveyor2 or 
            self.OMRON["Estado robot"]==self.EstadosROBOT.EnCaminoaABBPlace or self.OMRON["Estado robot"]==self.EstadosROBOT.DejandoEnABBPlace):
                self.robotEnTarea2 = 3
                self.estadoActivoT2 = self.OMRON["Estado robot"]
            else:
                self.robotEnTarea2 = 0
                self.estadoActivoT2 = None

            #Verifica si el OMRON esta haciendo la Tarea 3
            if (self.OMRON["Estado robot"]==self.EstadosROBOT.EnCaminoaABBPick or self.OMRON["Estado robot"]==self.EstadosROBOT.RecogiendoEnABBPick or 
            self.OMRON["Estado robot"]==self.EstadosROBOT.EnCaminoaAlmacen or self.OMRON["Estado robot"]==self.EstadosROBOT.DejandoEnAlamcen):
                self.robotEnTarea3 = 3
                self.estadoActivoT3 = self.OMRON["Estado robot"]
            else:
                self.robotEnTarea3 = 0
                self.estadoActivoT3 = None

        else:
            errConOm +=1
            if errConOm == 5:
                self.error("No se pudo establecer conexión con el servidor OMRON",1)

    def escrituraServidor(self, registros, valores):
        self.server.write_multiple_registers(registros,valores)
        
    def Detenido(self): #FALTA MODIFICAR
        #Mandar a Todo a STOP
        print("Detenido")

    def EnReposo(self):
        if (self.SMART1["Estado robot"] != self.EstadosROBOT.Charging):
            self.escrituraServidor[self.dir.EstadoSMART1,[self.EstadosROBOT.EnCaminoaHOME]]
        if (self.SMART2["Estado robot"] != self.EstadosROBOT.Charging):
            self.escrituraServidor[self.dir.EstadoSMART2,[self.EstadosROBOT.EnCaminoaHOME]]
        if self.registros[self.dir.InstruccionPLC] != 0:
            self.escrituraServidor(self.dir.InstruccionPLC,[0])
        if self.registros[self.dir.InstruccionABB] != 0:
            self.escrituraServidor(self.dir.InstruccionABB,[0])
        if self.señalModula == 1:
            self.escrituraServidor(0,[2])
            time.sleep(1)

    def EnOperacion(self):
        if self.señalModula == 1: #Cuando se instruya a sacar material del Modula, se le dan las instrucciones por Modbus de sacar el fixture
            if self.operacionModula == False and self.robotEnTarea1==0:
                self.serverModula.write_multiple_registers(0,self.instModula.PedirMaterial)
                self.serverModula.write_single_coil(0,1)
                time.sleep(0.5)
                self.operacionModula = True
            elif self.operacionModula == True:
                if self.comprobacionModula == False:
                    self.serverModula.write_multiple_registers(0,self.instModula.RevisionEstado)
                    self.serverModula.write_single_coil(0,1)
                    time.sleep(2)
                    try:
                        señalmodula = self.serverModula.read_input_registers(0,5)
                        if señalmodula[0]==2:
                            self.comprobacionModula = True
                            self.materialListo = True
                    except:
                        pass

        if self.materialListo == True: #Cuando el fixture del Modula esta disponible se Inicia la Tarea 1 y se regresa la charola del Modula
            if self.robotEnTarea1 == 0: #Si ningun SMART esta haciendo la Tarea 1
                if self.SMART1Libre and self.SMART2Libre:
                    if (self.SMART1["Bateria"] > self.SMART2["Bateria"]):
                        if self.contadorTareasS1 < (self.contadorTareasS2 + 1):
                            self.escrituraServidor(self.dir.EstadoSMART1,[self.EstadosROBOT.EnCaminoaModula])
                            self.Tarea1 = True
                            self.contadorTareasS1+=1
                        else:
                            self.escrituraServidor(self.dir.EstadoSMART2,[self.EstadosROBOT.EnCaminoaModula])
                            self.Tarea1 = True
                            self.contadorTareasS2+=1
                    elif (self.SMART1["Bateria"] < self.SMART2["Bateria"]):
                        if self.contadorTareasS2 < (self.contadorTareasS1 + 1):
                            self.escrituraServidor(self.dir.EstadoSMART2,[self.EstadosROBOT.EnCaminoaModula])
                            self.Tarea1 = True
                            self.contadorTareasS2+=1
                        else:
                            self.escrituraServidor(self.dir.EstadoSMART1,[self.EstadosROBOT.EnCaminoaModula])
                            self.Tarea1 = True
                            self.contadorTareasS1+=1
                elif self.SMART1Libre:
                    self.escrituraServidor(self.dir.EstadoSMART1,[self.EstadosROBOT.EnCaminoaModula])
                    self.contadorTareasS1+=1
                    self.Tarea1 = True
                elif self.SMART2Libre:
                    self.escrituraServidor(self.dir.EstadoSMART2,[self.EstadosROBOT.EnCaminoaModula])
                    self.contadorTareasS2+=1
                    self.Tarea1 = True
            elif self.robotEnTarea1 == 1:
                if self.SMART1["Estado robot"] == EstadosROBOT.EnCaminoaConveyor1:
                    self.serverModula.write_multiple_registers(0,self.instModula.ConfirmarOperacion)
                    self.serverModula.write_single_coil(0,1)
                    self.operacionModula = False
                    self.materialListo = False
                    self.comprobacionModula = False
                    self.server.write_single_register(1,0)
                    time.sleep(1)
            elif self.robotEnTarea1 == 2:
                if self.SMART2["Estado robot"] == EstadosROBOT.EnCaminoaConveyor1:
                    self.serverModula.write_multiple_registers(0,self.instModula.ConfirmarOperacion)
                    self.serverModula.write_single_coil(0,1)
                    self.operacionModula = False
                    self.materialListo = False
                    self.comprobacionModula = False
                    self.server.write_single_register(1,0)
                    time.sleep(1)

        if self.Tarea1 == True: #Lógica para detectar el cambio de estados que da fin a la Tarea 1 e inicia el Proceso 1
            if (self.memoriaTarea1 == self.EstadosROBOT.DejandoEnConveyor1) and (self.memoriaTarea1 != self.estadoActivoT1):
                #Significa que hubo un cambio de estado de dejando en conveyor a Libre
                self.Tarea1 = False #Se acaba la Tarea 1
                self.Proceso1 = True #Inicia el Proceso 1
                self.memoriaTarea1 = None
            else:
                self.memoriaTarea1 = self.estadoActivoT1
        
        if self.Proceso1 == True: #Manda la instrucción de Inicio al PLC y monitorea su estado para terminar el proceso e iniciar Tarea 2
            if self.estadoConveyor == 0:
                self.escrituraServidor(self.dir.InstruccionPLC,[1])
            elif self.estadoConveyor == 1:
                self.escrituraServidor(self.dir.InstruccionPLC,[0])
            elif self.estadoConveyor == 7: #Depende de la indormación que mande el PLC
                self.Proceso1 = False
                self.Tarea2 = True

        if self.Tarea2 == True: #Comprobación cambio de estado Tarea 2
            if (self.memoriaTarea2 == self.EstadosROBOT.DejandoEnABBPlace) and (self.memoriaTarea2 != self.estadoActivoT2):
                #Significa que hubo un cambio de estado de dejando en ABB Place a Libre
                self.Tarea2 = False #Se acaba la Tarea 2
                self.Proceso2 = True #Inicia el Proceso 2
                self.memoriaTarea2 = None
            else:
                self.memoriaTarea2 = self.estadoActivoT2   
        
        if self.Tarea2 == True: #Manda un robot a hacer la Tarea 2 y monitorea los estados para darle fin a la Tarea 2 y empezar el Proceso 2
            if self.robotEnTarea2 == 0: #Si ningun SMART esta haciendo la Tarea 2
                if self.OMRONLibre:
                    self.serverOMRON.write_single_register(5,self.EstadosROBOT.EnCaminoaConveyor2)

        if self.Proceso2 == True: #Manda la instrucción de Inicio al ABB y monitorea su estado para terminar el proceso e iniciar Tarea 3
            if self.estadoABB == 0:
                self.escrituraServidor(self.dir.InstruccionABB,[1])
            elif self.estadoABB == 1:
                self.escrituraServidor(self.dir.InstruccionABB,[0])
            elif self.estadoABB == 2: #Depende de la indormación que mande el PLC respecto al ABB
                self.Proceso2 = False
                self.Tarea3 = True

        if self.Tarea3 == True: #Comprobación cambio de estado de Tarea 3
            if (self.memoriaTarea3 == self.EstadosROBOT.DejandoEnAlamcen) and (self.memoriaTarea3 != self.estadoActivoT3):
                #Significa que hubo un cambio de estado de dejando en ABB Place a Libre
                self.Tarea3 = False #Se acaba la Tarea 2
                self.memoriaTarea3 = None
                self.verificarFin = True
                self.escrituraServidor(self.dir.InfoAlmacen,[1])
            else:
                self.memoriaTarea3 = self.estadoActivoT3
        
        if self.Tarea3 == True: #Manda un robot a hacer la Tarea 3 y monitorea los estados para darle fin a la Tarea 3 y darle fin al proceso activo de SF
            if self.robotEnTarea3 == 0: #Si ningun SMART esta haciendo la Tarea 3
                if self.OMRONEsperando:
                    self.serverOMRON.write_single_register(5,self.EstadosROBOT.EnCaminoaABBPick)

        if self.verificarFin == True:
            #Tal vez se pueden meter más condiciones de verificación como esperar a que los robots esten en charging, o algo así.
            self.escrituraServidor(0,[3])
            time.sleep(1)
            self.verificarFin = False

    def Terminado(self):
        print("Proceso Terminado, se procede a esperar")
        time.sleep(2)
        self.escrituraServidor(0,[1])
        
    def Run(self):
        self.lecturaServidor()
        if self.estadoSF == self.EstadosSF["Detenido"]:
            self.Detenido()
        elif self.estadoSF == self.EstadosSF["En Reposo"]:
            self.EnReposo()
        elif self.estadoSF == self.EstadosSF["En Operacion"]:
            self.EnOperacion()
        elif self.estadoSF == self.EstadosSF["Terminado"]:
            self.Terminado()
        else:
            self.error("Estado de Smart Factory no reconocido")
        
    def error(self, msg="", serv=0):
        if msg != "":
            msg = ": " + msg
        print("Ha ocurrido un error" + msg)
        if serv != 1:
            print("Ultima instancia leida: ")
            print(self.registros)
        exit()
        
    
c=Control()
while True:
    c.Run()
