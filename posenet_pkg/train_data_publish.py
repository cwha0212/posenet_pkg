#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose


class TrainDataPublisher(Node):

  def __init__(self):
    super().__init__('tain_data_publish_node')

    self.publisher = self.create_publisher(Pose, 'train_pose', 10)

    self.get_logger().info('Node Started, Waiting.... \n')

    self.metadata_path = "/root/gcamp_ros2_ws/src/gcamp_ros2_basic/posenet_pkg/posenet_pkg/data/dataset_train.txt"
    raw_lines = open(self.metadata_path, 'r',encoding='latin1').readlines()
    self.lines = raw_lines[3:]

    self.poses = []
    self.num = 0

    for i, line in enumerate(self.lines):
      splits = line.split()
      values = splits[1:]
      values = list(map(lambda x: float(x.replace(",", "")), values))
      self.poses.append(values)
      self.num += 1

  def publish(self):
    msg = Pose()
    for i in self.num
      msg.position.x = float(self.poses[i][0])
      msg.position.y = float(self.poses[i][1])
      msg.position.z = float(self.poses[i][2])
      msg.orientation.x = float(self.poses[i][4])
      msg.orientation.y = float(self.poses[i][5])
      msg.orientation.z = float(self.poses[i][6])
      msg.orientation.w = float(self.poses[i][3])
      self.publisher.publish(msg)
      self.get_logger().info(f'{i} Publish Done! \n')

def main(args=None):

  rclpy.init(args=args)

  train_data_publisher = TrainDataPublisher()

  train_data_publisher.publish()

  rclpy.shutdown()


if __name__ == '__main__':
  main()