#!/usr/bin/env python2
import time
import sys
import rospy
import tf
from std_msgs.msg import String,Int32,Int16 ,Float32
from std_msgs.msg import Int32MultiArray as HoldingRegister
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import *
from nav_msgs.msg import Path
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal,MoveBaseActionGoal,MoveBaseActionResult
from dashgo_tools.srv import *
import math
from InfoSMART import EstadosSMART, Coordenadas, Rutinas
import subprocess

initial_position = None
class StateMachine:
    def __init__(self):
        self.battery_status = rospy.Subscriber("voltage_percentage", Int32, self.batterycallback)
        self.estatus_mision=rospy.Subscriber('/move_base/status', GoalStatusArray, self.status_callback)
        self.instrucciones_server = rospy.Subscriber("instruccion_s",Int16,self.instruccioncallback)
        self.mission_status = rospy.Publisher("missionstatus",Int16 ,queue_size=10)
        self.auto_recharge = rospy.Publisher("recharge_handle", Int16, queue_size=10) 
        self.goal_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=5)
        
        self.oldcoordinatex = 0.0
        self.oldcoordinatey = 0.0
        self.oldcoordinatez = 0.0
        self.distancegoal= 0.0
        self.cont=0
        self.batterypercentage=100
        self.manualmode=False
        self.newgoal = 0
        self.mission="Move"
        self.goal = MoveBaseActionGoal()
        self.nextmisssion=True
        self.newcoordinatesvec=Vector3()
        self.oldcoordinatesvec=Vector3(0,0,0)
        
        self.station=[
            [-5.91625070572,5.34506416321,0.000000,0.000000,0.00000,-0.710403,0.703795]
            ]
        self.current_node=None
        self.estadoActual = None


    def status_callback(self, msg):
        try:
            self.estatus_mision = msg.status_list[0].status
        except:
            pass
    def batterycallback(self, msg):
        self.batterypercentage=msg.data
    def instruccioncallback(self,msg):
        self.instruccion = msg.data
    def serviceRobotRec(self, req):
        confirmacion = req.a
        if confirmacion == 1:
            self.serv.shutdown()
        return InfoStatRobotResponse(self.statusRobot)
    def robotRobotStatus(self, statusRobot): #serviceRobotSend
        self.serv = rospy.Service('status_robot', InfoStatRobot, self.serviceRobotRec)
        self.statusRobot = statusRobot
        self.serv.spin()
    def robotServerStatus(self):
        rospy.wait_for_service('status_server')
        try:
            Proxy = rospy.ServiceProxy('status_server', InfoStatServer)
            conf = Proxy(1)
            return conf.b
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
    def sendGoal2(self,goal_position):
        quaternion = Quaternion()
        self.goal.header.frame_id="map"
        self.goal.header.stamp=rospy.Time.now()
        self.goal.goal_id.stamp=rospy.Time.now()
        self.goal.goal_id.id=str(rospy.Time.now().to_sec())
        self.goal.goal.target_pose.header.frame_id = 'map'
        self.goal.goal.target_pose.header.stamp = rospy.Time.now()
        quaternion.x = float(goal_position[3])
        quaternion.y = float(goal_position[4])
        quaternion.z = float(goal_position[5])
        quaternion.w = float(goal_position[6])
        self.goal.goal.target_pose.pose.position.x = float(goal_position[0])
        self.goal.goal.target_pose.pose.position.y = float(goal_position[1])
        self.goal.goal.target_pose.pose.position.z = float(goal_position[2])
        self.goal.goal.target_pose.pose.orientation = quaternion
        self.goal_pub.publish(self.goal)
        rospy.logwarn(self.goal)

    def EnCaminoA(self, coordenadas, nuevoestado):
        robot.auto_recharge.publish(0)
        listener = tf.TransformListener()
        robot.sendGoal2(coordenadas)
        rospy.sleep(3)
        if robot.estatus_mision == GoalStatus.SUCCEEDED:
            robot.estadoActual = nuevoestado
            self.mission_status.publish(3)#####
    
    def rutinaxArm(self, rutina, nuevoestado):
        robot.current_node = subprocess.Popen('exec ' + rutina, stdout=subprocess.PIPE, shell = True )
        robot.current_node.wait()
        robot.estadoActual = nuevoestado
        self.mission_status.publish(3) ########
    
    def go_chargestation(self):
        listener = tf.TransformListener()
        if self.manualmode==True:
            angle = 70 * math.pi/180
            ax = self.station[0][0]
            ay = self.station[0][1]
        else:
            angle = 30 * math.pi/180
            ax = self.newcoordinatesvec.x
            ay= self.newcoordinatesvec.y
        a = [ ax, ay,0.000,0.000,0.000,0.000,0.000] #Ax,Ay,Az,qx,qy,qz,qw
        a[3] = 0.000
        a[4] = 0.000
        a[5] = math.sin(angle/2)
        a[6] = math.cos(angle/2)
        if self.nextmisssion==1:
            self.sendGoal2(a)
            self.distancegoal = 0
            self.nextmisssion=2
        if self.mission==0 and self.nextmisssion==2:
            self.robot_status.publish(0)
            rospy.sleep(3)
            self.auto_recharge.publish(1)
        elif self.mission==1 or self.mission==2 and self.nextmisssion==2:
            self.nextmisssion=1
 
if __name__ == '__main__':
    try:
        rospy.init_node('statemachine')
        robot = StateMachine()
        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():

            robot.estadoActual = robot.robotServerStatus()
            if robot.batterypercentage >= 50:
                if robot.estadoActual == EstadosSMART.Reset:
                    rospy.loginfo("Reset")
                elif robot.estadoActual == EstadosSMART.Charging:
                    rospy.loginfo("Charging")
                    if robot.instruccion == 1:
                        robot.estadoActual = EstadosSMART.EnCaminoaModula
                    if robot.instruccion == 2:
                        robot.estadoActual = EstadosSMART.EnCaminoaConveyor2
                    if robot.instruccion == 3:
                        robot.estadoActual = EstadosSMART.EnCaminoaABBPick
                    else:
                        rospy.loginfo("Instruccion no reconocida")
                elif robot.estadoActual == EstadosSMART.EnCaminoaModula:
                    rospy.loginfo("En Camino a Modula")
                    robot.EnCaminoA(Coordenadas.Modula, EstadosSMART.RecogiendoEnModula)
                elif robot.estadoActual == EstadosSMART.RecogiendoEnModula:
                    rospy.loginfo("Recogiendo en Modula")
                    robot.rutinaxArm(Rutinas.RecogiendoEnModula,EstadosSMART.EnCaminoaConveyor1)
                elif robot.estadoActual == EstadosSMART.EnCaminoaConveyor1:
                    rospy.loginfo("En Camino a Conveyor 1")
                    robot.EnCaminoA(Coordenadas.Conveyor1, EstadosSMART.DejandoEnConveyor1)
                elif robot.estadoActual == EstadosSMART.DejandoEnConveyor1:
                    rospy.loginfo("Dejando en Conveyor 1")
                    robot.rutinaxArm(Rutinas.DejandoEnConveyor1,EstadosSMART.Libre)
                elif robot.estadoActual == EstadosSMART.Libre:
                    rospy.loginfo("Libre")
                    if robot.instruccion == 1:
                        robot.estadoActual = EstadosSMART.EnCaminoaHOME
                    elif robot.instruccion == 2:
                        robot.estadoActual = EstadosSMART.EnCaminoaConveyor2
                    elif robot.instruccion == 3:
                        robot.estadoActual = EstadosSMART.EnCaminoaABBPick
                    else:
                        rospy.loginfo("Instruccion No Reconocida")
                elif robot.estadoActual == EstadosSMART.EnCaminoaHOME:
                    rospy.loginfo("En Camino a HOME")
                    # robot.go_chargestation()
                    # robot.estadoActual = EstadosSMART.Charging
                    robot.EnCaminoA(Coordenadas.HOME, EstadosSMART.Charging)
                elif robot.estadoActual == EstadosSMART.EnCaminoaConveyor2:
                    rospy.loginfo("En Camino a Conveyor 2")
                    robot.EnCaminoA(Coordenadas.Conveyor2, EstadosSMART.RecogiendoEnConveyor2)
                elif robot.estadoActual == EstadosSMART.RecogiendoEnConveyor2:
                    rospy.loginfo("Recogiendo en Conveyor 2")
                    robot.rutinaxArm(Rutinas.RecogiendoEnConveyor2,EstadosSMART.EnCaminoaABBPlace)
                elif robot.estadoActual == EstadosSMART.EnCaminoaABBPlace:
                    rospy.loginfo("En Camino a ABB Place")
                    robot.EnCaminoA(Coordenadas.ABBPlace,EstadosSMART.DejandoEnABBPlace)
                elif robot.estadoActual == EstadosSMART.DejandoEnABBPlace:
                    rospy.loginfo("Dejando en ABB Place")
                    robot.rutinaxArm(Rutinas.DejandoEnABBPlace, EstadosSMART.Libre)
                elif robot.estadoActual == EstadosSMART.EnCaminoaABBPick:
                    rospy.loginfo("En Camino a ABB Pick")
                    robot.EnCaminoA(Coordenadas.ABBPick, EstadosSMART.RecogiendoEnABBPick)
                elif robot.estadoActual == EstadosSMART.RecogiendoEnABBPick:
                    rospy.loginfo("Recogiendo en ABB Pick")
                    robot.rutinaxArm(Rutinas.RecogiendoEnABBPick, EstadosSMART.Libre)
                elif robot.estadoActual == EstadosSMART.EnCaminoaAlmacen:
                    rospy.loginfo("En Camino a Almacen")
                    robot.EnCaminoA(Coordenadas.Almacen, EstadosSMART.DejandoEnAlamcen)
                elif robot.estadoActual == EstadosSMART.DejandoEnAlamcen:
                    rospy.loginfo("Dejando en Almacen")
                    robot.rutinaxArm(Rutinas.DejandoEnAlmacen, EstadosSMART.Libre)
                else:
                    rospy.loginfo("Sin Estado Definido")
                robot.robotRobotStatus(robot.estadoActual)

            else:
                rospy.loginfo("Bateria menor al 50%")
                #Ir a charging
            r.sleep()
        #robot.current_node.terminate()
    except rospy.ROSInterruptException:
        rospy.logerr("Navigation test finished.")
