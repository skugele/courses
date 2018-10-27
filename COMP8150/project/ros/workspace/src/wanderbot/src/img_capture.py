#! /usr/bin/env python

import rospy
import cv2
import cv_bridge
from sensor_msgs.msg import Image

dest_dir = '/var/local/data/skugele/COMP8150/project/images'
raw_image_topic = '/camera/rgb/image_raw'
img_bridge = cv_bridge.CvBridge()
save_freq = 100
recv_count = 0
n_saved_images = 0


def save_image_to_disk(img_msg):
    global n_saved_images

    n_saved_images += 1
    cv_image = img_bridge.imgmsg_to_cv2(img_msg, desired_encoding='bgr8')

    filename = '/'.join([dest_dir, 'image_{}.png'.format(n_saved_images)])
    cv2.imwrite(filename, cv_image)


def receive_msg(data):
    global recv_count

    if data:
        recv_count += 1
        rospy.loginfo('Received: ' + str(data.header.seq))

        # Only save 1 of "save_freq" images to disk
        if recv_count % save_freq == 1:
            save_image_to_disk(data)


if __name__ == '__main__':
    rospy.init_node('img_capture')

    rospy.loginfo('img_capture node starting')
    rospy.Subscriber(raw_image_topic, data_class=Image, callback=receive_msg, queue_size=1)

    rospy.spin()
