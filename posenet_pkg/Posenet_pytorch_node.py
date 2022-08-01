#!/usr/bin/env python3

import sys

sys.path.append('/root/gcamp_ros2_ws/src/gcamp_ros2_basic/posenet_pkg/posenet_pkg')

from geometry_msgs.msg import Pose
from sensor_msgs.msg import Image as Images
import rclpy
from rclpy.node import Node

import cv2
from cv_bridge import CvBridge
import numpy as np
from PIL import Image
from torch.backends import cudnn

from node_data_loader import get_loader
from node_solver import Solver

class PosenetNode(Node):

  def __init__(self):
    super().__init__('posenet_node')

    self.publisher = self.create_publisher(Pose, 'posenet_pytorch', 10)

    self.subscriber = self.create_subscription(Images, 'image/cv2', self.sub_callback, 10)

    self.br = CvBridge()
    
    self.get_logger().info('Node Started, Waiting.... \n')

  def sub_callback(self, msg):
    
    opencv_img = self.br.imgmsg_to_cv2(msg)
    cvt_img = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cvt_img)
    cudnn.benchmark = True
    data_loader = get_loader(image=pil_img,model='Resnet',mode='test', batch_size=1)
    self.get_logger().info('data load complete! \n')

    solver = Solver(data_loader)
    self.get_logger().info('solver continue...! \n')

    pos, ori = solver.test()
    self.get_logger().info('test complete! \n')
    pose_msg = Pose()
    pose_msg.position.x = float(pos[0])
    pose_msg.position.y = float(pos[1])
    pose_msg.position.z = float(pos[2])
    pose_msg.orientation.x = float(ori[1])
    pose_msg.orientation.y = float(ori[2])
    pose_msg.orientation.z = float(ori[3])
    pose_msg.orientation.w = float(ori[0])

    self.get_logger().info(f'position [x:{pose_msg.position.x}, y:{pose_msg.position.y}, z:{pose_msg.position.z}]')
    self.get_logger().info(f'orientation [x:{pose_msg.orientation.x}, y:{pose_msg.orientation.y}, z:{pose_msg.orientation.z}, w:{pose_msg.orientation.w}]')
    self.get_logger().info('====Done====')



def main(args=None):

  rclpy.init(args=args)
  posenet_node = PosenetNode()

  rclpy.spin(posenet_node)

  rclpy.shutdown()
  print("done")


if __name__ == '__main__':
  main()
