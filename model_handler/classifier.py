"""
CLASSIFIER COMPONENT

CONTRIBUTORS:
    Paul Durham
	
FILE CONTENT DESCRIPTION:
The contents of the classifier file utilize information garnered from the trained model perform
accurate classifications regarding the contents of the camera frames retrieved from the USB camera.
Additionally, various methods from the cv2 library are utilized to normalize the camera frames, providing
the system model with a uniform data set to further increase the system's accuracy. 
[Paul please elaborate more about specificities.......]

REQUIREMENTS ADDRESSED:
    FR.3, FR.4 
    NFR.2, NFR.3, NFR.4

CORRESPONDING SDD SECTIONS: 
Processing narrative for Classifier Object - 3.2.1.C
Classifier Object Interface Description - 3.2.2.C
Classifier Object processing detail  - 3.2.3.C
Restrictions/limitations for Classifier Object - 3.2.3.2.C
Performance issues for Classifier Object - 3.2.3.3.C
Processing detail for each operation of Classifier Object - 3.2.3.5.C
Processing narrative for each operation - 3.2.3.5.1.C
Algorithmic model for each operation - 3.2.3.5.2.C

LICENSE INFORMATION:
    Copyright (c) 2019, CSC 450 Group 1
    All rights reserved.
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:
        * Redistributions of source code must retain the above copyright notice, this list of conditions and the
          following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
          the following disclaimer in the documentation and/or other materials provided with the distribution.
        * Neither the name of the CSC 450 Group 4 nor the names of its contributors may be used to endorse or
          promote products derived from this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import sys
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
            try:
                ## Loading model
                self.model = torch.hub.load('pytorch/vision:v0.5.0', 'alexnet', pretrained=True)
                self.model.load_state_dict(torch.load('model.pt'))
                self.model.eval()
            except:
                print('System model not detected, please assure that "model.pt" is downloaded..')
                sys.exit(1)
        ## Creates a transformer object.
        ## This transformer does the following, resizes the image and crops to the resize. Grayscales it.  transforms it to a tensor object and normalizes the pixel values
        self.trans = transforms.Compose([
            transforms.Resize(224),
            transforms.Grayscale(num_output_channels=3),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([.5, 0.5, 0.5], [0.5, 0.5, 0.5])
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
