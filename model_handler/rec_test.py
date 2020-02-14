import torch
from torchvision.transforms import transforms
from PIL import Image
from pathlib import Path
import os
from torchvision import datasets, models, transforms
import torch.nn as nn
import numpy as np
from matplotlib import cm
import cv2
#global vars
# onOrOffFan = 0
# onOrOffLights = 0

class Classifer:
    def __init__(self):
        self.model = models.resnet18(pretrained=True)
        self.set_parameter_requires_grad(True)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 2)
        self.model.load_state_dict(torch.load('C:/Users/paulr/projects/450/ASL-Controlled-Smart-Home-Environment/model_handler/resnet.pt'))
        self.model.eval()
        self.trans = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.Resize(32),
            transforms.CenterCrop(32),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def classify(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_new = Image.fromarray(img)
        input = self.trans(img_new)
        input = input.view(1, 3, 32, 32)
        output = self.model(input)
        prediction = int(torch.max(output.data, 1)[1].numpy())
        print("prediction = "+str(prediction))
        ##return prediction

    def set_parameter_requires_grad(self, feature_extracting):
        if feature_extracting:
            for param in self.model.parameters():
                param.requires_grad = False

