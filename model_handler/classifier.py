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

## Classifier class that can classify ASL alphabet gestures
class Classifier:
    ## __init__ function for class sets up class variables.
    def __init__(self):
        ## these are the potential labels for objects
        self.labels = ['1','2','3','A','B', 'C']
        ## This try/except statement is if you are running the file itself to run the test method or importing it. The model.pt will be different location based on the context of who calls it. 
        try:
            ## Loading model
            self.model = torch.hub.load('pytorch/vision:v0.5.0', 'alexnet', pretrained=True)
            self.model.load_state_dict(torch.load('model_handler/model.pt'))
            self.model.eval()
        except Exception:
            ## Loading model
            self.model = torch.hub.load('pytorch/vision:v0.5.0', 'alexnet', pretrained=True)
            self.model.load_state_dict(torch.load('model.pt'))
            self.model.eval()
        ## Creates a transformer object.
        ## This transformer does the following, resizes the image and crops to the resize. Grayscales it.  transforms it to a tensor object and normalizes the pixel values
        self.trans = transforms.Compose([
            transforms.Resize(224),
            transforms.Grayscale(num_output_channels=3),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    ## This function takes a frame from cv2 and attempts to classify it.
    def classify(self,img):
        img_new = Image.fromarray(img)
        ## Transforms the img file
        input = self.trans(img_new)
        ## This ensures the img is the right shape for the classification
        input = input.unsqueeze(0)
        ## classifies the img
        cls = self.model.eval()(input)
        ## Finds the output values
        output = torch.nn.Softmax()(cls.float())
        ## Finds the highest predicted label
        max_probability , predicted = torch.max(output, 1)
        ## Removes the probability from the tensor object
        max_probability = max_probability.data.cpu().numpy()[0]
        ## Finds the label as predicted is the index value of the predicted
        res = self.labels[predicted]
        ## If the probability is over the threshold
        if max_probability > .7:
            return res
        else:
           return None


    def set_parameter_requires_grad(self, feature_extracting):
        if feature_extracting:
            for param in self.model.parameters():
                param.requires_grad = False
                
    ## This is a testing method to find the classifications for all images in a set of folders.
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
        print("correct="+str(correct))

## If the .py is ran directly this will run and attempt to classify everything image in the test folder.
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
