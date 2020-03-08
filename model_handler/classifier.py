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
        self.labels = ['1','2','3','A','B', 'C']
        try:
            self.model = torch.load('model_handler/model.pt')
        except Exception:
            self.model = torch.load('model.pt')
        self.trans = transforms.Compose([
            transforms.Resize(224),
            transforms.Grayscale(num_output_channels=3),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def classify(self,img):
        img_new = Image.fromarray(img)
        input = self.trans(img_new)
        input = input.unsqueeze(0)
        cls = self.model.eval()(input)
        output = torch.nn.Softmax()(cls.float())
        max_probability , predicted = torch.max(output, 1)
        max_probability = max_probability.data.cpu().numpy()[0]
        res = self.labels[predicted]
        if max_probability > .50:
            print(res)
            return res
        else:
            print(output)
        return None

    def set_parameter_requires_grad(self, feature_extracting):
        if feature_extracting:
            for param in self.model.parameters():
                param.requires_grad = False

    def test(self, paths):
        correct = 0
        total = 0
        for x in paths:
            img = Image.open(x)
            img = self.trans(img)
            img = img.unsqueeze(0)
            res = self.model.eval()(img)
            output = torch.nn.Softmax()(res.float())
            max_probability , predicted = torch.max(output, 1)
            max_probability = max_probability.data.cpu().numpy()[0]
            res = self.labels[predicted]
            print(x)
            x = x.split("--")[1]

            if x == res:
                print(res+" == "+x)
                print(output)
                correct += 1
            else:
                print(res+"!="+x)
                print(output)
            total += 1
            ##_, indices = torch.sort(res, descending=True)
            ##percentage = torch.nn.functional.softmax(res, dim=1)[0] * 100
        print("Total="+str(total))
        print("correct"+str(correct))

if __name__ == "__main__":
    ## begin test ##
    files = []
    cls = Classifier()
    path = "testing_dataset/"

    for r, d, f in os.walk(path):
        for file in f:
            if '.jpg' in file:
                files.append(os.path.join(r, file))
            if '.png' in file:
                files.append(os.path.join(r, file))

    cls.test(files)
