#!/usr/bin/env python
import cv2
import rospy
import time
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class EasyCap:
    def __init__(self, cam_num):
        self.cap = cv2.VideoCapture()
        self.cap.open(cam_num, apiPreference=cv2.CAP_V4L2)
        if not self.cap.isOpened():
            rospy.logfatal('Could not open capture device %d', cam_num)
            print('couldnot open')
        rospy.init_node("EasyCapFPV")
        
        self.bridge = CvBridge()
        self.easycap_publisher = rospy.Publisher("easycap", Image, queue_size=1)
        
    def ros_stream(self):
        while not rospy.is_shutdown():
            ret, frame = self.cap.read()
            if not ret:
                rospy.logdebug('EASYCAP: no frame avaliable')
                continue
            image_msg = self.bridge.cv2_to_imgmsg(frame)
            self.easycap_publisher.publish(image_msg)

    def window_stream(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                cv2.imshow('easycap', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print('Dropped Frame')
            
if __name__ == '__main__':
    cam_index = int(sys.argv[1])
    rospy.loginfo('EASYCAP: using camera %d', cam_index)
    print(cam_index)
    cap = EasyCap(cam_index)
    cap.ros_stream()
