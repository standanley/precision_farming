from PIL import Image

'''
img = Image.new( 'RGB', (255,255), "black") # create a new black image
pixels = img.load() # create the pixel map

for i in range(img.size[0]):    # for every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 100) # set the colour accordingly

img.show()

exit()
'''
'''
im = Image.open('big.tif')
region = im.crop((4000, 4000, 4100, 4100))
regionrgb = region.convert('RGB')
regionrgb.save('small.png')
'''
im = Image.new( 'RGB', (100,100), "black")
x = im.load()

for i in range(100):
	for j in range(100):
		x[i,j] = (2*i, 255-2*j, 127)
im.show()