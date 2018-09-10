#!/usr/bin/env python

import rospy
# import csv
import os
# import atexit
# import sys
import message_filters
import subprocess
# import roslib
# roslib.load_manifest('fingervision_msgs')
from geometry_msgs.msg import WrenchStamped
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
# from fingervision_msgs.msg import BlobMoves
# from fingervision_msgs.msg import Filter1Wrench

dir_rosbag = '/media/song/disk/food_manipulation/tactile/fingervision/calib_data/rosbag/'

trial = 1

def saveRosbag(trial):
    # if not os.path.exists(directory_rosbag):
    #     os.makedirs(directory_rosbag)
    # # subprocess.call
    subprocess.Popen('rosbag record /fingervision/fv_3_l/blob_moves /fingervision/fv_3_l/wrench /fingervision/fv_3_l/fv_3_l/image_raw /fingervision/fv_3_r/blob_moves /fingervision/fv_3_r/wrench /fingervision/fv_3_r/fv_3_r/image_raw /fingervision/fv_filter1_wrench -O ' + dir_rosbag + str(trial), shell=True)

def saveData():
    print('saveData')
    global trial
    # generate a directory
    if not os.path.exists(dir_rosbag):
        os.makedirs(dir_rosbag)
    
    while os.path.isfile(dir_rosbag+str(trial)+".bag"):
        trial = trial + 1
    # data_file = open(directory+str(trial)+".csv",'w')
    # writer = csv.writer(data_file,delimiter=',')
    print('Save to '+str(trial)+'.bag')
    saveRosbag(trial)

def callback():
    print("callback")
    saveData()   

def listener():
    
    rospy.init_node('listener', anonymous=True,  disable_signals=True)
    # print("init node")

    # fv_l_blob_sub = message_filters.Subscriber("fingervision/fv_3_l/blob_moves", BlobMoves) 
    fv_l_wrench_sub = message_filters.Subscriber("fingervision/fv_3_l/wrench", WrenchStamped) 
    fv_l_image_sub = message_filters.Subscriber("fingervision/fv_3_l/fv_3_l/image_raw", Image)
    # fv_r_blob_sub = message_filters.Subscriber("fingervision/fv_3_r/blob_moves", BlobMoves) 
    fv_r_wrench_sub = message_filters.Subscriber("fingervision/fv_3_r/wrench", WrenchStamped) 
    fv_r_image_sub = message_filters.Subscriber("fingervision/fv_3_r/fv_3_r/image_raw", Image)
    # fv_wrench_sub = message_filters.Subscriber("fingervision/fv_filter1_wrench", Filter1Wrench)
    # forque_sub = message_filters.Subscriber("ft_sensor/netft_data", WrenchStamped) 
    print('Subscriber')
    ts = message_filters.ApproximateTimeSynchronizer([fv_l_wrench_sub, fv_l_image_sub, fv_r_wrench_sub, fv_r_image_sub], queue_size=5, slop=0.1)
    ts.registerCallback(callback)
    print("registerCallback")
    rospy.spin()
    print("spin")

if __name__ == '__main__':
    print("listener!")
    listener()
