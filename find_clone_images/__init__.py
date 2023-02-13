
from image_hashing import dhash_z_transformed as hash_image
from os import listdir, path, mkdir, rename, walk

# for every file in the directory, hash it, and set the filepath as the value, and the hash as the key
# if any files match an already existing one, move both images into a folder

valid_file_types = [".jpg", ".jpeg", ".png", ".webp", ".PNG", ".JPG", ".JPEG"]
def isValidFileType(file):
	for valid_type in valid_file_types:
		if file.endswith(valid_type):
			return True
	return False

def assort_directory(search_directory, clone_directory, move_original_with_clones=False):
	if not path.exists(clone_directory):
		mkdir(clone_directory)

	hash_dict = { }
	for file in listdir(search_directory):
		if not isValidFileType(file):
			continue
		try:
			hashed_result = hash_image(path.join(search_directory, file))
			if hashed_result in hash_dict.keys():
				# move original clone to folder
				original_path = hash_dict.get(hashed_result)
				if move_original_with_clones and path.exists( original_path ):
					_, tail = path.split( original_path )
					rename(original_path, path.join(clone_directory, tail))
				# move new clone to folder
				rename( path.join(search_directory, file), path.join(clone_directory, file) )
			else:
				# add to hash dict
				hash_dict[hashed_result] = path.join(search_directory, file)
		except Exception as e:
			print("Skipped error; ", e)
			pass

def assort_descendants(parent_directory, clone_directory, move_original_with_clones=False):
	if not path.exists(clone_directory):
		mkdir(clone_directory)

	hash_dict = { }
	for root, dirs, files in walk(parent_directory):
		for file in files:
			if not isValidFileType(file):
				continue
			try:
				hashed_result = hash_image(path.join(root, file))
				if hashed_result in hash_dict.keys():
					# move original clone to folder
					original_path = hash_dict.get(hashed_result)
					if move_original_with_clones and path.exists( original_path ):
						_, tail = path.split( original_path )
						rename(original_path, path.join(clone_directory, tail))
					# move new clone to folder
					rename( path.join(root, file), path.join(clone_directory, file) )
				else:
					# add to hash dict
					hash_dict[hashed_result] = path.join(root, file)
			except Exception as e:
				print("Skipped error; ", e)
				pass

search_directory = input("Input the filepath to search; ")
search_type = input("Input 1 for direct children of parent, otherwise anything else for descendants of parent.")
clone_directory = input("Input a folder name for any clone images; ")
if search_type == "1":
	assort_directory(search_directory, path.join(search_directory, clone_directory))
else:
	assort_descendants(search_directory, path.join(search_directory, clone_directory))
