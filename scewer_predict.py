#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import WrenchStamped

init_value_R = 0
init_value_L = 0
n = 0
m = 0
th = 0.006
numSample = 20

def callbackR(data):
    global init_value_R, n

    # rospy.loginfo(rospy.get_caller_id() + "I heard %f", data.wrench.force.x)
    
    if n<numSample:
        init_value_R = init_value_R + data.wrench.force.x
    elif n==numSample:
        init_value_R = init_value_R/numSample
        print("Initialized!")
    else:
        weight = init_value_R - data.wrench.force.x
        if weight > th:
            print("[R] Scewered!")
        else:
            print("[R] Nothing!")
    n = n+1

def callbackL(data):
    global init_value_L, m

    # rospy.loginfo(rospy.get_caller_id() + "I heard %f", data.wrench.force.x)
    
    if m<numSample:
        init_value_L = init_value_L + data.wrench.force.x
    elif m==numSample:
        init_value_L = init_value_L/numSample
        print("Initialized!")
    else:
        weight = - (init_value_L - data.wrench.force.x)
        if weight > th:
            print("[L]          Scewered!")
        else:
            print("[L]          Nothing!")
    m = m+1

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    

    rospy.Subscriber("fingervision/fv_3_r/wrench", WrenchStamped, callbackR)
    # rospy.Subscriber("fingervision/fv_3_l/wrench", WrenchStamped, callbackL)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    # global init_value
    listener()
    
