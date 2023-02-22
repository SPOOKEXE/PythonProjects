
from image_hashing import dhash_z_transformed as hash_image
from os import listdir, path, mkdir, rename, walk
from concurrent import futures as futures
from json import dumps

WORKER_COUNT = 25
HASH_DICT = {}

valid_file_types = [".jpg", ".jpeg", ".png", ".webp", ".PNG", ".JPG", ".JPEG"]
def isValidFileType(file):
	for valid_type in valid_file_types:
		if file.endswith(valid_type):
			return True
	return False

# multi-thread this
def hash_image_from_filepath(filepath):
	try:
		hash_value = hash_image(filepath)
		return does_dict_contain_hash(hash_value), filepath
	except:
		pass
	return False, filepath

def does_dict_contain_hash(hash_value : str) -> bool:
	hash_value = str(hash_value)
	splitA = hash_value[:4]
	splitB = hash_value[4:]
	if not HASH_DICT.get(splitA):
		HASH_DICT[splitA] = [splitB]
		return False
	if HASH_DICT.get(splitA).count(splitB) == 0:
		HASH_DICT.get(splitA).append(splitB)
		return False
	return True

def find_clone_files(file_absolute_paths, output_directory):
	TOTAL_IMAGE_FILES = len(file_absolute_paths)
	TOTAL_IMAGES_REMAINING = TOTAL_IMAGE_FILES
	TOTAL_CLONE_IMAGES = 0

	executor = futures.ThreadPoolExecutor(max_workers=WORKER_COUNT)

	promises = []
	for absfile in file_absolute_paths:
		promises.append(executor.submit(hash_image_from_filepath, absfile))

	for promise in futures.as_completed(promises):
		result, filepath = promise.result()
		if result == True:
			TOTAL_CLONE_IMAGES += 1
			try:
				rename( filepath, path.join(output_directory, path.basename(filepath)) )
			except:
				pass
		TOTAL_IMAGES_REMAINING -=1
		print("Awaiting " + str(TOTAL_IMAGES_REMAINING) + " images to be compared - found " + str(TOTAL_CLONE_IMAGES) + " clones so far.")

	with open('dump.json', 'w') as file:
		file.write( dumps(HASH_DICT) )

def assort_directory(search_directory, output_directory):
	if not path.exists(output_directory):
		mkdir(output_directory)

	absolute_filepaths = []
	files = listdir( search_directory )
	for file in files:
		if not isValidFileType(file):
			continue
		absolute_filepaths.append( path.join(search_directory, file) )

	HASH_DICT = {}
	find_clone_files(absolute_filepaths, output_directory)

def assort_descendants(parent_directory, output_directory):
	if not path.exists(output_directory):
		mkdir(output_directory)

	absolute_filepaths = []
	for root, dirs, files in walk(parent_directory):
		for file in files:
			if not isValidFileType(file):
				continue
			abspath = path.join(root, file)
			absolute_filepaths.append( abspath )

	HASH_DICT = {}
	find_clone_files(absolute_filepaths, output_directory)
