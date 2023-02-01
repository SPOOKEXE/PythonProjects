
from os import listdir, path
from PIL import Image

# for every file in the directory, hash it, and set the filepath as the value, and the hash as the key
# if any files match an already existing one, move both images into a folder

search_directory = input("Input the directory to sort; ")

valid_file_types = [".jpg", ".jpeg", ".png", ".webp", ".PNG", ".JPG", ".JPEG"]
def isValidFileType(file):
	for valid_type in valid_file_types:
		if file.endswith(valid_type):
			return True
	return False

for file in listdir(search_directory):
	if isValidFileType(file):
		img = Image.open( path.join(search_directory, file) )
		width = str(img.width)
		height = str(img.height)

		if not path.exists("dim_" + width + "_" + height):
			path.mkdir("dim_" + width + "_" + height)

		filedata = None
		with open(path.join(search_directory, file), "rb") as f:
			filedata = f.read()

		with open(path.join("dim_" + width + "_" + height, file), "wb") as f:
			f.write(filedata)
