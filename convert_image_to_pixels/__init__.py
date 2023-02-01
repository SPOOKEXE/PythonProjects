
from PIL import Image
from numpy import array as np_array
import numpy

print("What is your image file name and extension?")
print("Example:  image.png")
filename = input("")
pixels = None
try:
	img = Image.open(filename)
	pixels = np_array(img).tolist()
except IOError:
	print("File not accessible")
finally:
	img.close()

if pixels == None:
	print("Could not get the pixels.")
else:
	a_file = open("output.lua", "w")
	lines = ["local pixels = {"]
	for row in pixels:
		lines.append("\n\t{")
		for pixel in row:
			lines.append("\n\t\t{" + "{}, {}, {}, {}".format(pixel[0], pixel[1], pixel[2],pixel[3] ) + "},")
		lines.append("\t}")
	lines.append("\n}")
	a_file.writelines( lines )
	a_file.close()
