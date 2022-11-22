#!/usr/bin/env python2
import time
import sys
import rospy
from std_msgs.msg import Int32,Int16,String
from nav_msgs.msg import Path
from geometry_msgs.msg import Vector3, Pose
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from std_msgs.msg import Int32MultiArray as HoldingRegister
from actionlib_msgs.msg import GoalStatus
from std_msgs.msg import Int16
from move_base_msgs.msg import MoveBaseActionGoal,MoveBaseActionResult
from dashgo_tools.srv import *
import math
class Server:
    def __init__(self):
        self.mission_status = rospy.Subscriber("mission_status", Int16, self.missioncallback)
        self.battery_status = rospy.Subscriber("voltage_percentage", Int32, self.batterycallback)
        self.pose=rospy.Subscriber("/robot_pose", Pose, self.positioncallback)
        self.robotStatus=0
        self.missionStatus=0
        self.batterypercentage=100
        self.registro = [0]
        ''''
        ROBOT STATUS / GOAL STATUS
            uint8 PENDING=0
            uint8 ACTIVE=1
            uint8 PREEMPTED=2
            uint8 SUCCEEDED=3
            uint8 ABORTED=4
            uint8 REJECTED=5
            uint8 PREEMPTING=6
            uint8 RECALLING=7
            uint8 RECALLED=8
            uint8 LOST=9
            actionlib_msgs/GoalID goal_id
            uint8 status
            string text
        '''
        #Registers (Not Updated): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, robotStatus, missionStatus, batteryPercentage, Goalx, Goaly, Currx, Curry]
        self.oldx=0
        self.oldy=0
        self.oldz=0

    def missioncallback(self, msg):
        self.missionStatus=msg.data
    def batterycallback(self, msg):
        self.batterypercentage=msg.data
    def positioncallback(self, msg):
        self.currx=msg.position.x
        self.curry=msg.position.y
        self.currz=msg.position.z
    def serviceServerRec(self, req):
        confirmacion = req.a
        if confirmacion == 1:
            self.serv.shutdown()
        return InfoStatServerResponse(self.statusServidor)
    def robotServerStatus(self, statusServ): #serviceServerSend
        self.serv = rospy.Service('status_server', InfoStatServer, self.serviceServerRec)
        self.statusServidor = statusServ
        self.serv.spin()
    def robotRobotStatus(self):
        rospy.wait_for_service('status_robot')
        try:
            Proxy = rospy.ServiceProxy('status_robot', InfoStatRobot)
            conf = Proxy(1)
            return conf.b
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
    def transformCoords(self):
        if self.currx < 0:
            coordX = (-self.currx * 1000) + 20000
        else:
            coordX = (self.currx * 1000) + 10000

        if self.curry < 0:
            coordY = (-self.curry * 1000) + 20000
        else:
            coordY = (self.curry * 1000) + 10000
        coords = [coordX, coordY]
        return coords


    

if __name__ == '__main__':
    try:
        rospy.init_node('Server_info')
        robot = Server()
        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            try:
                client =  ModbusClient("192.168.31.9",port=12345) #Server second computer
                UNIT = 0x1
                conexion = client.connect()
                rospy.logwarn("Modbus connection ready")
            except Exception as error:
                rospy.logwarn("Modbus connection error")
                rospy.logwarn(error)
            try:
                rr = client.read_holding_registers(0,19,unit=UNIT)
                robot.registro = rr.registers
                rospy.logwarn("Del servidor: %s", rr.registers)
                rospy.logwarn("Info robot working")
                #ROS Service que manda info del servidor al Robot
                robot.robotServerStatus(robot.registro[5])
                robot.robotStatus = robot.registro[5]
                #ROS Service que recibe la información del Robot
                robotr_status = robot.robotRobotStatus()
                pose_coords = robot.transformCoords()
                if robot.robotStatus != robotr_status:
                        robot.robotStatus = robotr_status
                robot.registro[5] = robot.robotStatus
                robot.registro[6] = robot.missionStatus
                robot.registro[7] = robot.batterypercentage
                robot.registro[10] = pose_coords[0] #x
                robot.registro[11] = pose_coords[1] #y
                updateRegister1 = [robot.registro[5], robot.registro[6], robot.registro[7]]
                updateRegister2 = [robot.registro[10], robot.registro[11]]
                client.write_registers(5, updateRegister1, unit=UNIT)
                client.write_registers(10, updateRegister2, unit=UNIT)
                client.close()
                rospy.sleep(0.5)
                                    
            except Exception as error:
                rospy.logwarn("Reading registers not ready")
                rospy.logwarn(error)  
                rospy.sleep(1)
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")