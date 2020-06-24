import torch
from torch import nn
from train import play

torch.manual_seed(0)

model = nn.Sequential(nn.Linear(14, 128), nn.ReLU(),
                      nn.Linear(128, 128), nn.ReLU(),
                      nn.Linear(128, 128), nn.ReLU(),
                      nn.Linear(128, 1)
                     )
model.load_state_dict(torch.load("train1000.pth"))

play("greedy", "random_walk")