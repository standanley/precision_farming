from PIL import Image

folder = 'data/p1/'

MINK = 1


locationsX = [93, 54, 27, 104, 76, 53, 27, 106, 83, 59, 27, 6, 27, 54, 104, 82, 53, 27, 27, 6, 6, 6, 127, 127, 127, 127, 127]
locationsY = [111, 111, 111, 81, 81, 81, 81, 21, 21, 31, 31, 19, 14, 7, 54, 54, 54, 58, 45, 57, 83, 108, 111, 80, 52, 35, 14]
locationsMagic = [(x, y) for x,y in zip(locationsX, locationsY)]
#print(locationsMagic)

# get num x num sensors
# only works for squares for now
def getLocations(im, num):
	pix = im.load()
	step = im.size[0] / (num+1)
	xlocations = range(step, im.size[0]-step/2, step)
	locations = []
	for x in xlocations:
		for y in xlocations:
			locations.append((x, y))
	return locations

def getReadings(im, locations):
	pix = im.load()
	readings = []
	for x,y in locations:
		readings.append((x, y, pix[x, y]))
	return readings

def rate(im1, im2):
	sum = 0
	dif = diff(im1, im2)
	#print('im1: ', im1)
	bdif = dif.load()
	for i in range(im1.size[0]):
		for j in range(im1.size[1]):
			sum += bdif[i, j]**2
	sum /= float(im1.size[0]*im1.size[1])
	return sum**0.5

def diff(im1, im2):
	#print('im1 diff: ', im1)
	res = Image.new('I;16', im1.size, 'black')
	#print('type of im1', type(im1))
	b1 = im1.load()
	b2 = im2.load()
	bres = res.load()
	for i in range(im1.size[0]):
		for j in range(im1.size[1]):
			bres[i,j] = b1[i, j] - b2[i,j]
	return res

def add(im1, im2):
	#print('im1 add: ', im1)
	res = Image.new('I;16', im1.size, 'black')
	b1 = im1.load()
	b2 = im2.load()
	bres = res.load()
	for i in range(im1.size[0]):
		for j in range(im1.size[1]):
			bres[i,j] = b1[i, j] + b2[i,j]
	return res

def copy(im1):
	#print('im1 add: ', im1)
	res = Image.new('I;16', im1.size, 'black')
	b1 = im1.load()
	bres = res.load()
	for i in range(im1.size[0]):
		for j in range(im1.size[1]):
			bres[i,j] = b1[i, j]
	return res

def linear(im1, im2):
	#print('im1 lin: ', im1)
	temp = diff(im2, im1)
	res = add(im2, temp)
	return res

def interpolate(im1, readings):
	im = copy(im1)
	if len(readings) == 0:
		return im
	pix = im.load()
	corrections = [(x, y, v-pix[x,y]) for x,y,v in readings]

	for i in range(im1.size[0]):
		for j in range(im1.size[1]):
			csum = 0
			wsum = 0
			for x,y,c in corrections:
				if i==x and j==y:
					pix[i, j] += c
					wsum = -1
					break
				weight = 1.0/((x-i)**2 + (y-j)**2)**(float(MINK)/2)
				wsum += weight
				csum += weight * c
			if wsum != -1:
				correction = csum / wsum
				pix[i, j] += int(correction)
	return im


def interpolate2(im1, readings):
	im = copy(im1)
	if len(readings) == 0:
		return im
	pix = im.load()
	corrections = [(x, y, v-pix[x,y]) for x,y,v in readings]

	for i in range(im1.size[0]):
		for j in range(im1.size[1]):
			temp = [(((x-i)**2 + (y-j)**2), x, y, c) for x, y, c in corrections]
			_1, _2, _3, myc = min(temp)
			pix[i, j] += int(myc)
	return im



def testInterpolate(num, locations=None):
	sum = 0
	for i in range(1,12):

		im1 = Image.open(folder+'t0_b'+str(i)+'.tif')
		im2 = Image.open(folder+'t1_b'+str(i)+'.tif')
		im3 = Image.open(folder+'t2_b'+str(i)+'.tif')

		if not locations:
			locations = getLocations(im1, num)

		#print("Test nothing", rate(im3, im3))
		#print("Test im2", rate(im2, im3))
		#print("Test linear", rate(linear(im1, im2), im3))
		sum += rate(interpolate(im2, getReadings(im3, locations)), im3)
		#print('only v3')
	return sum / 11


for MINK in range(0,4):
	nums = []
	vs = []
	for i in range(1,2):
		#print(MINK, i)
		nums.append(i**2)
		vs.append(testInterpolate(i, locationsMagic))
		#print(nums[-1], vs[-1])
	print('MINK:\t'+str(MINK))
	print(vs)