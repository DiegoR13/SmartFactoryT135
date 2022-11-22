#!/usr/bin/env python2
class EstadosSMART:
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

class Coordenadas:
    #Ax,Ay,Az,qx,qy,qz,qw
    Modula = [2.2019, 3.1188, 0, 0, 0, 0.5786, 0.8155]
    Conveyor1 = [2.2019, 3.1188, 0, 0, 0, 0.5786, 0.8155]
    ABBPick = [2.2019, 3.1188, 0, 0, 0, 0.5786, 0.8155]
    HOME = [2.2019, 3.1188, 0, 0, 0, 0.5786, 0.8155]
    Conveyor2 = [2.2019, 3.1188, 0, 0, 0, 0.5786, 0.8155]
    ABBPlace = [2.2019, 3.1188, 0, 0, 0, 0.5786, 0.8155]
    Almacen = [2.2019, 3.1188, 0, 0, 0, 0.5786, 0.8155]

class Rutinas:
    RecogiendoEnModula = "python3 /home/eaibot/dashgo_ws/src/dashgo/xArm-Python-SDK/example/wrapper/xarm6/E3T/Rutina_1Eq3T.py"
    DejandoEnConveyor1 = "python3 /home/eaibot/dashgo_ws/src/dashgo/xArm-Python-SDK/example/wrapper/xarm6/E3T/Rutina_1Eq3T.py"
    RecogiendoEnConveyor2 = "python3 /home/eaibot/dashgo_ws/src/dashgo/xArm-Python-SDK/example/wrapper/xarm6/E3T/Rutina_1Eq3T.py"
    DejandoEnABBPlace = "python3 /home/eaibot/dashgo_ws/src/dashgo/xArm-Python-SDK/example/wrapper/xarm6/E3T/Rutina_1Eq3T.py"
    RecogiendoEnABBPick = "python3 /home/eaibot/dashgo_ws/src/dashgo/xArm-Python-SDK/example/wrapper/xarm6/E3T/Rutina_1Eq3T.py"
    DejandoEnAlmacen = "python3 /home/eaibot/dashgo_ws/src/dashgo/xArm-Python-SDK/example/wrapper/xarm6/E3T/Rutina_1Eq3T.py"