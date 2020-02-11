import torch
from torchvision.transforms import transforms
from PIL import Image
from pathlib import Path
import os

def get_files(path):
	dir =path
	res = []
	for root, dirs, files in os.walk(path):
		for file in files:
			res.append(os.path.join(root,file))
	return res

def run(path,model,trans):

	image = Image.open(path)

	input = trans(image)

	input = input.view(1, 3, 32,32)

	output = model(input)
	print(output)
	prediction = int(torch.max(output.data, 1)[1].numpy())
	return prediction


def main():
	model = torch.load('C:/Users/paulr/projects/450/ASL-Controlled-Smart-Home-Environment/model_handler/resnet.pt')

	trans = transforms.Compose([
    		transforms.RandomHorizontalFlip(),
    		transforms.Resize(32),
    		transforms.CenterCrop(32),
    		transforms.ToTensor(),
    		transforms.Normalize((0.5, 0.5, 0.5),(0.5, 0.5, 0.5))
    		])

	items = ['C:/Users/paulr/Documents/data-dir/train/asl_alphabet_train/A','C:/Users/paulr/Documents/data-dir/train/asl_alphabet_train/B']
	files = []
	result = 0
	total = 0
	for x in items:
		files.append(get_files(x))
	for x in range(2):
		for y in range(len(files[x])):
			
			if run(files[x][y],model,trans) == x:
				result+= 1
				total+=1
			else:
				total+=1
	print(total)
	print(result/total)
main()