from PIL import Image
import os
import re

# xmin, ymin, xmax, ymax

SIZE = 512
MINS = (5383-SIZE/2, 4208-SIZE/2) # upper left

# Add these to your coordinates to get to the same spot
XOFFSETS = [170, 60, 30, 0]
YOFFSETS = [10, 0, 10, 0]

id = 'p1'
folders = ['imgs1/', 'imgs2/', 'imgs3/', 'imgs4/']
images = []


def generate_cropped(mins):
	region = (MINS[0], MINS[1], MINS[0]+SIZE, MINS[1]+SIZE)

	for i in range(4):
		folder = folders[i]
		print(folder)
		for filepath in os.listdir(folder):
			tokens = re.split('_|\\.', filepath)
			if(len(tokens) < 2):
				continue
			if(tokens[-1] != 'TIF'):
				continue
			if(tokens[-2] != 'B5'):
				continue
			newregion = (region[0] + XOFFSETS[i], region[1] + YOFFSETS[i], region[2] + XOFFSETS[i], region[3] + YOFFSETS[i])
			
			im = Image.open(folder+filepath)
			print(tokens[-2], im.format, im.size, im.mode)
			
			cropped = im.crop(newregion)
			savename = 'data/'+"_".join([id, str(i), tokens[-2]])+'.tif'
			print(savename)
			cropped.save(savename)

generate_cropped(MINS)