#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from time import sleep

from geometry_msgs.msg import PoseArray, Pose


class DataPublisher(Node):

  def __init__(self):
    super().__init__('data_publish_node')

    self.publisher = self.create_publisher(PoseArray, 'train_pose', 10)

    self.get_logger().info('Node Started, Waiting.... \n')

    self.metadata_path = "/root/KingsCollege/dataset_test.txt"
    raw_lines = open(self.metadata_path, 'r',encoding='latin1').readlines()
    self.lines = raw_lines[3:]

    self.train_poses = []
    self.num = []

    for i, line in enumerate(self.lines):
      splits = line.split()
      values = splits[1:]
      values = list(map(lambda x: float(x.replace(",", "")), values))
      self.train_poses.append(values)
      self.num.append(i)

  def publish(self):
    val = Pose()
    msg = PoseArray()
    for i in self.num:
      val.position.x = self.train_poses[i][0]
      val.position.y = self.train_poses[i][1]
      val.position.z = self.train_poses[i][2]
      val.orientation.x = self.train_poses[i][4]
      val.orientation.y = self.train_poses[i][5]
      val.orientation.z = self.train_poses[i][6]
      val.orientation.w = self.train_poses[i][3]
      msg.poses.append(val)
      msg.header.frame_id = "/my_frame"
      sleep(0.2)
    self.publisher.publish(msg)
    self.get_logger().info('Publish Done!! \n')


def main(args=None):

  rclpy.init(args=args)

  data_publisher = DataPublisher()

  data_publisher.publish()

  rclpy.shutdown()


if __name__ == '__main__':
  main()