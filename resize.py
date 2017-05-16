from PIL import Image
import os
import re


for i in range(4, 5):
	folder = 'imgs'+str(i)+'/'
	for filepath in os.listdir(folder):
		tokens = re.split('_|\\.', filepath)
		if(len(tokens) < 2):
			continue
		if(tokens[-1] != 'TIF'):
			continue
		if tokens[-2] == 'B8':
			# rescale
			print(folder+filepath)
			imf = open(folder+filepath, 'rb')
			im = Image.open(imf)
			newsize = [x/2 for x in im.size]
			print(newsize)
			smaller = im.resize(newsize)
			imf.close()
			os.rename(folder+filepath, folder+'new_'+filepath)
			smaller.save(folder+filepath)