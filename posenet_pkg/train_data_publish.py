#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from time import sleep

from geometry_msgs.msg import PoseArray, Pose


class TrainDataPublisher(Node):

  def __init__(self):
    super().__init__('train_data_publish_node')

    self.publisher = self.create_publisher(Pose, 'train_pose', 10)

    self.get_logger().info('Node Started, Waiting.... \n')

    self.metadata_path = "/root/KingsCollege/dataset_train.txt"
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
    # msg = PoseArray()
    val = Pose()
    # msg.poses = []
    for i in self.num:
      val.position.x = self.train_poses[i][0]
      val.position.y = self.train_poses[i][1]
      val.position.z = self.train_poses[i][2]
      val.orientation.x = self.train_poses[i][4]
      val.orientation.y = self.train_poses[i][5]
      val.orientation.z = self.train_poses[i][6]
      val.orientation.w = self.train_poses[i][3]
      # msg.poses.append(val)
      self.publisher.publish(val)
      sleep(0.05)
      self.get_logger().info(f'{i} \n')

    # self.publisher.publish(msg)
    self.get_logger().info('Publish Done!! \n')


def main(args=None):

  rclpy.init(args=args)

  train_data_publisher = TrainDataPublisher()

  train_data_publisher.publish()

  rclpy.shutdown()


if __name__ == '__main__':
  main()