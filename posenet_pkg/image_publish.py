#!/usr/bin/env python3

from sensor_msgs.msg import Image
import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge

class ImagePublisher(Node):

  def __init__(self):
    super().__init__('image_node')

    self.publisher = self.create_publisher(Image, 'image/cv2', 10)

    self.get_logger().info('Node Started, Waiting.... \n')

    self.image = cv2.imread('/root/gcamp_ros2_ws/src/gcamp_ros2_basic/posenet_pkg/posenet_pkg/image/test.png')
    self.br = CvBridge()

  def publish(self):
    msg = Image()
    msg = self.br.cv2_to_imgmsg(self.image)
    self.publisher.publish(msg)
    self.get_logger().info('Publish Done! \n')



def main(args=None):

  rclpy.init(args=args)

  image_publisher = ImagePublisher()

  image_publisher.publish()
  image_publisher.destroy_node()

  rclpy.shutdown()


if __name__ == '__main__':
  main()
