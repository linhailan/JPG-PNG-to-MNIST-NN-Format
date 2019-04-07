import os
from PIL import Image
from array import *
from random import shuffle

width = 255
height = 255

# Load from and save to
Names = [['./training-images','train'], ['./test-images','test']]
for name in Names:
	
	data_image = array('B')
	data_label = array('B')

	FileList = []
	labeldictionarylist = {}
	j = 0
	for dirname in os.listdir(name[0]):
		labeldictionarylist[dirname]=j
		j += 1
		path = os.path.join(name[0],dirname)
		for filename in os.listdir(path):
			if filename.endswith(".jpg"):
				FileList.append(os.path.join(name[0],dirname,filename))

	shuffle(FileList) # Usefull for further segmenting the validation set

	i = 0
	for filename in FileList:
		if i % 100 == 0:
			print("file:" ,i)

		label = labeldictionarylist[filename.split('/')[2]]

		Im = Image.open(filename)
		ResizeIm = Im.resize((width,height))

		pixel = ResizeIm.load()
		for x in range(0,width):
			for y in range(0,height):
				data_image.append(pixel[y,x])

		data_label.append(label)
		i += 1

	hexval = "{0:#0{1}x}".format(len(FileList),6) # number of files in HEX

	# header for label array
	header = array('B')
	header.extend([0,0,8,1,0,0])
	header.append(int('0x'+hexval[2:][:2],16))
	header.append(int('0x'+hexval[2:][2:],16))

	data_label = header + data_label
	print("data_label:",data_label)

	# additional header for images array
	
	if max([width,height]) < 256:
		header.extend([0,0,0,width,0,0,0,height])
	else:
		raise ValueError('Image exceeds maximum size: 256x256 pixels');

	header[3] = 3 # Changing MSB for image data (0x00000803)
	print("header:",header)

	data_image = header + data_image
	print("data_image:",data_image[:128])

	imagesfile = name[1]+'-images-idx3-ubyte'
	if os.path.exists(imagesfile):
		os.remove(imagesfile)
	output_file = open(imagesfile, 'wb')
	data_image.tofile(output_file)
	output_file.close()

	labelsfile = name[1]+'-labels-idx1-ubyte'
	if os.path.exists(labelsfile):
		os.remove(labelsfile)
	output_file = open(labelsfile, 'wb')
	data_label.tofile(output_file)
	output_file.close()

# gzip resulting files
for name in Names:
	os.system('gzip -f '+name[1]+'-images-idx3-ubyte')
	os.system('gzip -f '+name[1]+'-labels-idx1-ubyte')
