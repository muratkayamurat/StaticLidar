#!/usr/bin/env python

import rospy
import tf2_ros
from sensor_msgs.msg import LaserScan, Range
import time
import array
from math import sin, cos, atan2, pi, sqrt
from hiddriver import hiddriver
import numpy as np

TEST1 = 0
TEST2 = 1
MEASURING = 2


class staticlidardriver():
    def __init__(self,modulename = "SeomakStaticLidar"):
        self.staticlidarhid = hiddriver(modulename)
        rospy.init_node(modulename)
        if not (self.staticlidarhid.productFound):
            print("%s module not found"%(modulename))
        else:
            print("static lidar driver started")
            self.num_readings = 9
            self.lidar_freq = 20
            self.ranges = np.zeros(self.num_readings)
            self.intensities = np.zeros(self.num_readings)
            self.state = ""
            self.reading = True
            self.dataready = False
            
            
            self.scan_pub = rospy.Publisher('/staticlidar/scan', LaserScan, queue_size=10)
            
            self.stamp = rospy.Time.now()    

    def error_control(self):
        pass

    def shutdown(self):
        pass

    def read_data(self,length):
    # def read_data(self):
        # print("manuel driver reading started")
        # while(self.reading):
        #self.dataready=False
        dataf = np.zeros(9)
        scanStr = ""
        #self.distances = np.zeros(4)
        #self.distances_id = np.zeros(4)
        scanStr = self.staticlidarhid.read_device(64)
        if(scanStr == ""):
            self.dataready = False
            pass
            #self.errorCode = 16
        else:
            datas = scanStr.split(',')
            dataf = map(float, datas[0:9])
            print(dataf)
            self.ranges[0] = dataf[0]/1000
            self.ranges[1] = dataf[1]/1000
            self.ranges[2] = dataf[2]/1000
            self.ranges[3] = dataf[3]/1000
            self.ranges[4] = dataf[4]/1000
            self.ranges[5] = dataf[5]/1000
            self.ranges[6] = dataf[6]/1000
            self.ranges[7] = dataf[7]/1000
            self.ranges[8] = dataf[8]/1000
            self.dataready = True
            self.staticScanData = LaserScan()
            self.staticScanData.header.stamp = rospy.Time.now()
            self.staticScanData.header.frame_id = "base_link"
            self.staticScanData.angle_min = -170*(pi/180)
            self.staticScanData.angle_max = 10*(pi/180)
            self.staticScanData.angle_increment = 20*(pi/180)
            self.staticScanData.time_increment = 0.05 #sec
            self.staticScanData.range_min = 0
            self.staticScanData.range_max = 4.5
            self.staticScanData.ranges = [self.ranges[8],self.ranges[7],self.ranges[6],self.ranges[5],self.ranges[4],self.ranges[3],self.ranges[2],self.ranges[1],self.ranges[0]]
            self.staticScanData.intensities = [self.ranges[8],self.ranges[7],self.ranges[6],self.ranges[5],self.ranges[4],self.ranges[3],self.ranges[2],self.ranges[1],self.ranges[0]]
            
            self.scan_pub.publish(self.staticScanData)


if __name__ == '__main__':
    mcd = staticlidardriver()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mcd.read_data(64)
        rate.sleep()
    mcd.shutdown() 
