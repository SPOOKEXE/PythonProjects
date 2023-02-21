
from os import listdir, path, mkdir, rename, walk
from json import dumps

WORKER_COUNT = 25

valid_file_types = [".jpg", ".jpeg", ".png", ".webp", ".PNG", ".JPG", ".JPEG"]
def isValidFileType(file):
	for valid_type in valid_file_types:
		if file.endswith(valid_type):
			return True
	return False

def find_clone_files(file_absolute_paths, output_directory):
	counter = 1
	for absfile in file_absolute_paths:
		_, head = path.split(absfile)
		name, extension = path.splitext(head)
		name.replace(".", "_")
		rename( absfile, path.join(output_directory, str(counter) + extension) )
		counter += 1

def assort_directory(search_directory, output_directory):
	if not path.exists(output_directory):
		mkdir(output_directory)

	absolute_filepaths = []
	files = listdir( search_directory )
	for file in files:
		if not isValidFileType(file):
			continue
		absolute_filepaths.append( path.join(search_directory, file) )
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
	find_clone_files(absolute_filepaths, output_directory)

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
