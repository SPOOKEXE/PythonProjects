
from os import listdir, path
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

valid_file_types = [".jpg", ".jpeg", ".png", ".webp", ".PNG", ".JPG", ".JPEG"]
def isValidFileType(file):
	for valid_type in valid_file_types:
		if file.endswith(valid_type):
			return True
	return False

def assort_dir(directory, optimize=True): #, quality=80):
	for file in listdir(directory):
		if isValidFileType(file):
			img = Image.open( path.join(directory, file), formats=None )
			out_path = path.exists("dim_" + str(img.width) + "_" + str(img.height))
			if not out_path:
				path.mkdir(out_path)
			img.save(path.join(out_path, file), optimize=optimize) #, quality=80)

search_directory = input("Input the directory to sort; ")
assort_dir(search_directory)
