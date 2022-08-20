#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose
from visualization_msgs.msg import Marker, MarkerArray

class TrainDataRvizNode(Node):

  def __init__(self) -> None:
    super().__init__('train_data_rviz_node')

    self.publisher = self.create_publisher(Marker, 'train_marker', 10)

    self.subscriber = self.create_subscription(Pose, 'train_pose', self.sub_callback1, 10)
    self.subscriber = self.create_subscription(Pose, 'posenet_pytorch', self.sub_callback2, 10)
    self.num = 0
    self.get_logger().info('Node Started, Waiting.... \n')

  def sub_callback1(self, msg):

    marker_msg = Marker()
    image_pose = msg

    marker_msg.header.frame_id = "/my_frame"
    marker_msg.ns = "train_data"
    marker_msg.id = self.num
    marker_msg.type = Marker.ARROW
    marker_msg.action = Marker.ADD
    marker_msg.scale.x = 1.0
    marker_msg.scale.y = 0.1
    marker_msg.scale.z = 0.1
    marker_msg.color.a = 1.0
    marker_msg.color.r = 0.0
    marker_msg.color.g = 0.0
    marker_msg.color.b = 1.0
    marker_msg.pose = image_pose
    self.publisher.publish(marker_msg)
    self.num += 1

  def sub_callback2(self, msg):

    marker_msg = Marker()
    image_pose = msg

    marker_msg.header.frame_id = "/my_frame"
    marker_msg.ns = "train_data"
    marker_msg.id = self.num
    marker_msg.type = Marker.ARROW
    marker_msg.action = Marker.ADD
    marker_msg.scale.x = 1.0
    marker_msg.scale.y = 0.1
    marker_msg.scale.z = 0.1
    marker_msg.color.a = 1.0
    marker_msg.color.r = 0.0
    marker_msg.color.g = 1.0
    marker_msg.color.b = 0.0
    marker_msg.pose = image_pose
    self.publisher.publish(marker_msg)
    self.num += 1

def main(args=None):

  rclpy.init(args=args)
  train_data_rviz_node = TrainDataRvizNode()

  rclpy.spin(train_data_rviz_node)

  rclpy.shutdown()
  print("done")

if __name__ == '__main__':
  main()
