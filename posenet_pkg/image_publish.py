#!/usr/bin/env python3

import os
from sensor_msgs.msg import Image
import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge
from time import sleep

class ImagePublisher(Node):

  def __init__(self):
    super().__init__('image_node')

    self.publisher = self.create_publisher(Image, 'image/cv2', 10)

    self.get_logger().info('Node Started, Waiting.... \n')

    self.image_path = "/root/KingsCollege"
    self.metadata_path = "/root/KingsCollege/dataset_test.txt"
    raw_lines = open(self.metadata_path, 'r',encoding='latin1').readlines()
    self.lines = raw_lines[3:]

    self.train_filenames = []

    for i, line in enumerate(self.lines):
      splits = line.split()
      filename = splits[0]
      filename = os.path.join(self.image_path, filename)
      self.train_filenames.append(filename)

    self.br = CvBridge()

  def publish(self):
    msg = Image()
    for image in self.train_filenames:
      image_cv2 = cv2.imread(image)
      msg = self.br.cv2_to_imgmsg(image_cv2)
      self.publisher.publish(msg)
      sleep(1)
    self.get_logger().info('Publish Done! \n')



def main(args=None):

  rclpy.init(args=args)

  image_publisher = ImagePublisher()

  image_publisher.publish()

  rclpy.shutdown()


if __name__ == '__main__':
  main()
