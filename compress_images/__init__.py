from os import listdir, path, mkdir
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

valid_file_types = [".jpg", ".jpeg", ".png", ".webp", ".PNG", ".JPG", ".JPEG"]
def isValidFileType(file):
	for valid_type in valid_file_types:
		if file.endswith(valid_type):
			return True
	return False

def compress_filepaths(image_filepaths, out_directory):
	if not path.exists(out_directory):
		mkdir(out_directory)

	max_open_images = 1000
	filepath_to_array_data = {}
	counter = 0

	while len(image_filepaths) > 0:
		filepath = image_filepaths.pop()
		if path.exists( out_directory + "/" + path.basename(filepath) ):
			continue
		tempimg : Image.Image = Image.open(filepath, formats=None)
		filepath_to_array_data[filepath] = [tempimg.mode, tempimg.size, tempimg.tobytes()]
		counter += 1
		if counter < max_open_images:
			continue
		# reset counter
		counter = 0
		# compress open images
		while len(filepath_to_array_data.keys()) > 0:
			key, temp_array = filepath_to_array_data.popitem()
			(mode, size, byte_data) = tuple(temp_array)
			print(size, len(str(byte_data)))
			try:
				img = Image.frombytes(mode, size, byte_data)
				img.save(out_directory + "/" + path.basename(key), optimize=True, quality=80)
				img.close()
			except:
				pass
		print("Remaining Image Paths: " + str(len(image_filepaths)))

def scan_directory_for_images(directory):
	filepaths = []
	for file in listdir(directory):
		if isValidFileType(file):
			absPath = path.join(directory, file)
			filepaths.append(absPath)
	return filepaths

search_directory = input("Input the directory to compress; ")
abs_paths = scan_directory_for_images(search_directory)
compress_filepaths(abs_paths, path.join(search_directory, "compressed") )
