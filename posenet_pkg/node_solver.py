import os
import time
import numpy as np
import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.optim import lr_scheduler
from tensorboardX import SummaryWriter
from node_model import model_parser
from node_model import PoseLoss
from node_pose_utils import *

 

class Solver(): 
  def __init__(self, data_loader):
    self.data_loader = data_loader
    self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    self.model = model_parser(model='Resnet', fixed_weight=False, dropout_rate=0.5, bayesian = False)

  def test(self):

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    self.model = self.model.to(self.device)
    self.model.eval()
    test_model_path = '/root/gcamp_ros2_ws/src/gcamp_ros2_basic/posenet_pkg/posenet_pkg/model/best_net.pth'

    print('Load pretrained model: ', test_model_path)

    self.model.load_state_dict(torch.load(test_model_path))

    for i, inputs in enumerate(self.data_loader):
      inputs = inputs.to(self.device)
      pos_out, ori_out, _ = self.model(inputs)
      pos_out = pos_out.squeeze(0).detach().cpu().numpy()
      ori_out = F.normalize(ori_out, p=2, dim=1)
      ori_out = ori_out.squeeze(0).detach().cpu().numpy()
      print('pos_out', pos_out)
      print('ori_out', ori_out)

    return pos_out, ori_out