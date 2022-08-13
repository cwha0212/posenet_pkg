#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose
from visualization_msgs.msg import Marker, MarkerArray

class RvizMarkerNode(Node):

  def __init__(self) -> None:
    super().__init__('rviz_marker_node')

    self.publisher = self.create_publisher(Marker, 'marker', 10)

    self.subscriber = self.create_subscription(Pose, 'pose', self.sub_callback, 10)

    self.get_logger().info('Node Started, Waiting.... \n')

  def sub_callback(self, msg):

    marker_msg = Marker()
    image_pose = msg

    marker_msg.ns = "train_data"
    marker_msg.id = 1
    marker_msg.type = Marker.ARROW
    marker_msg.action = Marker.ADD
    marker_msg.pose = image_pose
    marker_msg.scale = Vector3(2,1,1)
    marker_msg.color = ColorRGBA(1,0,0,1)


def main(args=None):

  rclpy.init(args=args)
  rviz_marker_node = RvizMarkerNode()

  rclpy.spin(rviz_marker_node)

  rclpy.shutdown()
  print("done")

if __name__ == '__main__':
  main()
