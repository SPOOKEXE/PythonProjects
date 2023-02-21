
####
####	RESIZES IMAGES TO BE SMALLER THAN 1080p
####	AND COMPRESSES THEM WITH "optimize=True" AND "quality=80"
####

from os import path, mkdir, listdir, walk
from PIL import Image, ImageFile
from concurrent import futures as futures

ImageFile.LOAD_TRUNCATED_IMAGES = True

WORKER_COUNT = 25
ACTIVE_COUNTER = 0
ACTIVE_RESIZES = 0

DEFAULT_MAX_DIM = (1920, 1080)

VALID_IMAGE_FILE_TYPES = [".jpg", ".jpeg", ".png", ".webp", ".PNG", ".JPG", ".JPEG"]
def isValidFileType(file):
	global VALID_IMAGE_FILE_TYPES

	for valid_type in VALID_IMAGE_FILE_TYPES:
		if file.endswith(valid_type):
			return True
	return False

def isDimLarger(isThis : tuple[int, int], largerThanThis : tuple[int, int]) -> bool:
	return (isThis[0] > largerThanThis[0]) or (isThis[1] > largerThanThis[1])

def checkImageResize(abs_path : str, out_directory, max_dim : tuple[int, int]):
	global ACTIVE_RESIZES
	try:
		img = Image.open(abs_path, formats=None)
		filename = path.basename(abs_path)
		if isDimLarger(img.size, max_dim):
			ACTIVE_RESIZES += 1
			img.thumbnail(max_dim, Image.ANTIALIAS)
		img.save( path.join(out_directory, filename), optimize=True, quality=80)
		img.close()
	except Exception as e:
		print(e)
		pass

def scaleImagesToMaxDim(absolute_filepaths, out_directory, maxDim=DEFAULT_MAX_DIM):
	if absolute_filepaths == out_directory:
		return

	global WORKER_COUNT
	global ACTIVE_COUNTER
	global ACTIVE_RESIZES

	ACTIVE_RESIZES = 0
	TOTAL_IMAGES = 0
	ACTIVE_COUNTER = 0

	if not path.exists(out_directory):
		mkdir(out_directory)

	executor = futures.ThreadPoolExecutor(max_workers=WORKER_COUNT)

	# create all threads in threadpool for images
	future_promises = []
	for abs_path in absolute_filepaths:
		ACTIVE_COUNTER += 1
		future_promises.append(executor.submit(checkImageResize, abs_path, out_directory, maxDim))

	# wait for all threads to finish
	TOTAL_IMAGES = ACTIVE_COUNTER
	for promise in futures.as_completed(future_promises):
		print("Awaiting " + str(ACTIVE_COUNTER) + " threads to finish - resized a total of " + str(ACTIVE_RESIZES) + " images.")
		promise.result()
		ACTIVE_COUNTER -=1

	print("Completed checking and resizing " + str(TOTAL_IMAGES) + " images.")
	executor.shutdown()

def assort_directory(search_directory, output_directory, maxDim=DEFAULT_MAX_DIM):
	if not path.exists(output_directory):
		mkdir(output_directory)

	absolute_filepaths = []
	files = listdir( search_directory )
	for file in files:
		if not isValidFileType(file):
			continue
		absolute_filepaths.append( path.join(search_directory, file) )
	scaleImagesToMaxDim(absolute_filepaths, output_directory, maxDim=maxDim)

def assort_descendants(parent_directory, output_directory, maxDim=DEFAULT_MAX_DIM):
	if not path.exists(output_directory):
		mkdir(output_directory)

	absolute_filepaths = []
	for root, dirs, files in walk(parent_directory):
		for file in files:
			if not isValidFileType(file):
				continue
			abspath = path.join(root, file)
			absolute_filepaths.append( abspath )
	scaleImagesToMaxDim(absolute_filepaths, output_directory, maxDim=maxDim)

def default_switch_case_callback():
	pass

class SwitchCase:
	cases = {'default' : default_switch_case_callback}

	def Switch(self, value, *args, **kwargs):
		func = self.cases[value]
		if func:
			return func(*args, **kwargs)
		return self.cases['default'](*args, **kwargs)

	def Case(self, key, callback):
		key = str(key)
		if self.cases.get(key) and key != 'default':
			raise AssertionError("Key already exists in switch-case, use a different key.")
		self.cases[key] = callback

	def __init__(self):
		pass

if __name__ == '__main__':
	menu = SwitchCase()
	menu.Case('1', assort_descendants)
	menu.Case('2', assort_directory)

	# C:\Users\Declan\Pictures

	while True:
		print("Input the file path to search for images under.")
		search_directory = input()

		print("Input a folder name for compressed images to be stored in.")
		print("This will be placed in the folder of where the search is happening.")
		clone_directory_name = input()

		print("1 - Search all descendant folders for images.")
		print("2 - Search all directory children for images.")
		print("3 - Exit.")

		user_input = input("")
		if user_input == "3":
			exit()

		menu.Switch(user_input, search_directory, path.join(search_directory, clone_directory_name), maxDim=DEFAULT_MAX_DIM)
