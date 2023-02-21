
from .image_hashing import dhash_z_transformed as hash_image
from os import listdir, path, mkdir, rename, walk
from concurrent import futures as futures
from json import dumps

WORKER_COUNT = 25

valid_file_types = [".jpg", ".jpeg", ".png", ".webp", ".PNG", ".JPG", ".JPEG"]
def isValidFileType(file):
	for valid_type in valid_file_types:
		if file.endswith(valid_type):
			return True
	return False

# multi-thread this
def hash_image_from_filepath(filepath, hash_dict):
	try:
		hash_value = hash_image(filepath)
		return does_dict_contain_hash(hash_value, hash_dict)
	except:
		pass
	return False

def does_dict_contain_hash(hash_value : str, hash_dict : dict) -> bool:
	hash_value = str(hash_value)
	splitA = hash_value[:4]
	splitB = hash_value[4:]
	if not hash_dict.get(splitA):
		hash_dict[splitA] = []
	does_contain = True
	if hash_dict[splitA].count(hash_value) == 0:
		hash_dict[splitA].append(splitB)
		does_contain = False
	return does_contain

def find_clone_files(file_absolute_paths, output_directory, hash_dict = {}):
	TOTAL_IMAGE_FILES = len(file_absolute_paths)
	TOTAL_IMAGES_REMAINING = TOTAL_IMAGE_FILES
	TOTAL_CLONE_IMAGES = 0

	executor = futures.ThreadPoolExecutor(max_workers=WORKER_COUNT)

	promises = []
	for absfile in file_absolute_paths:
		promises.append(executor.submit(hash_image_from_filepath, absfile, hash_dict))

	for promise in futures.as_completed(promises):
		result = promise.result()
		if result == True:
			TOTAL_CLONE_IMAGES += 1
			rename( absfile, path.join(output_directory, path.basename(absfile)) )
		TOTAL_IMAGES_REMAINING -=1
		print("Awaiting " + str(TOTAL_IMAGES_REMAINING) + " images to be compared - found " + str(TOTAL_CLONE_IMAGES) + " clones so far.")

	with open('dump.json', 'w') as file:
		file.write( dumps(hash_dict) )

def assort_directory(search_directory, output_directory, hash_dict={}):
	if not path.exists(output_directory):
		mkdir(output_directory)

	absolute_filepaths = []
	files = listdir( search_directory )
	for file in files:
		if not isValidFileType(file):
			continue
		absolute_filepaths.append( path.join(search_directory, file) )
	find_clone_files(absolute_filepaths, output_directory, hash_dict={})

def assort_descendants(parent_directory, output_directory, hash_dict={}):
	if not path.exists(output_directory):
		mkdir(output_directory)

	absolute_filepaths = []
	for root, dirs, files in walk(parent_directory):
		for file in files:
			if not isValidFileType(file):
				continue
			abspath = path.join(root, file)
			absolute_filepaths.append( abspath )
	find_clone_files(absolute_filepaths, output_directory, hash_dict=hash_dict)

def default_switch_case_callback():
	pass

class SwitchCase:
	cases = {'default' : default_switch_case_callback}

	def Switch(self, value, *args):
		func = self.cases[value]
		if func:
			return func(*args)
		return self.cases['default'](*args)

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
		print("Input the file path to search for clone images under.")
		search_directory = input()

		print("Input a folder name for any cloned images to be stored in.")
		print("This will be in the root folder of where the search is happening.")
		clone_directory_name = input()

		print("1 - Search all descendant folders for clones.")
		print("2 - Search all directory children for clones.")
		print("3 - Exit.")

		user_input = input("")
		if user_input == "3":
			exit()

		menu.Switch(user_input, search_directory, path.join(search_directory, clone_directory_name))
