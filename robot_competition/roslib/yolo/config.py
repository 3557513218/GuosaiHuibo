import torch

import yaml
class Config:
    def __init__(self):
        self.dataset_path = ""
        self.learning_rate = 0.001
        self.epochs = 10
        self.batch_size = 32
        self.name = ""
        self.net = object

    def savemodel(self,net,path):
        torch.save(self.net,self.path)
# 创建全局配置对象
config = Config()
