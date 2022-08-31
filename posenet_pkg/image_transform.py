#!/usr/bin/env python3

import os
import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CompressedImage


class ImageTransform(Node):
  def __init__(self):
    super().__init__('image_transform_node')

    self.bridge = CvBridge()

    self.image_pub = self.create_publisher('/zed/left/image_rect_color/image', Image, queue_size = 1000)
    self.compressed_image_sub = self.create_subscriber('/zed/left/image_rect_color/compressed', CompressedImage, self.callback)
    self.num = 1
    
  def callback(self, data):
    cv_image = self.bridge.compressed_imgmsg_to_cv2(data, "bgr8")
    cv2.imwrite(f'/root/train_image/frame{self.num}.png',cv_image)
    self.get_logger().info('Done! \n')

def main(args=None):

  rclpy.init(args=args)

  image_tranform_node = ImageTransform()

  rclpy.spin(image_tranform_node)

  rclpy.shutdown()

if __name__ == '__main__':
  main()