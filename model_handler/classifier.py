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

class Classifier:
    def __init__(self):
        self.alphabet = ['A','B']
        self.model = models.resnet18(pretrained=True)
        self.set_parameter_requires_grad(True)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 2)
        # self.model.load_state_dict(torch.load('../model_handler/resnet.pt'))
        self.model.eval()
        self.trans = transforms.Compose([
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
        pred= torch.max(output.data, 1)[1].numpy()
        if int(torch.max(output.data[0])) >.10:

            return self.labels[pred.data[0]]

        return None

    def set_parameter_requires_grad(self, feature_extracting):
        if feature_extracting:
            for param in self.model.parameters():
                param.requires_grad = False

    def test(self, paths):
        for x in paths:
            img = self.Image.open(x)
            img = self.trans(img)
            img = img.unsqueeze(0)
            res = model(img)
            _, indices = torch.sort(res, descending=True)
            percentage = torch.nn.functional.softmax(res, dim=1)[0] * 100
            [(labels[idx], percentage[idx].item()) for idx in indices[0][:2]]

