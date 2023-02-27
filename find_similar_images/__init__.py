import numpy as np

from imagehash import average_hash, ImageHash
from concurrent import futures as futures
from PIL import Image, ImageFile
from os import path, listdir, rename, makedirs

ImageFile.LOAD_TRUNCATED_IMAGES = True

IMAGE_FILE_EXTENSIONS = [".jpg", ".png", ".jpeg", ".bmp", ".PNG", ".JPG", ".JPEG", ".BMP", ".webp", ".WEBP"]
def IsValidImageFile(filename_or_path) -> bool:
	for ext in IMAGE_FILE_EXTENSIONS:
		if filename_or_path.endswith(ext):
			return True
	return False

def _check_image_similarity(hash_1 : ImageHash, hash_2 : ImageHash, diff_limit : int):
	return np.count_nonzero(hash_1.hash != hash_2.hash) <= diff_limit

def get_diff_limit_from_similarity(similarity : int, hash_size=8) -> int:
	threshold = 1 - (similarity/100)
	diff_limit = int(threshold * (hash_size**2) )
	return diff_limit

def get_image_hash(filepath : str, hash_size) -> ImageHash:
	return average_hash(Image.open(filepath), hash_size)

def MoveSimilarImagesToDirectory( search_directory : str, dump_directory : str, similarity=98, hash_size=8) -> list[str]:
	makedirs(dump_directory, exist_ok=True)

	# get all the images in the directory
	image_files = []
	for filename in listdir(search_directory):
		if IsValidImageFile(filename):
			absolute_filepath = path.join( search_directory, filename )
			image_files.append( absolute_filepath )

	diff_limit = get_diff_limit_from_similarity(similarity, hash_size=hash_size)

	# do the actual hash check and parsing
	active_cache = { }

	# check each image hash against all other (active) hashes.
	count = 1
	for image_filepath in image_files:
		print(count, " / ", len(image_files))
		hash_1 = get_image_hash(image_filepath, hash_size)
		isSimilar = False
		for hash_2 in active_cache.values():
			isSimilar = _check_image_similarity(hash_1, hash_2, diff_limit)
			if isSimilar:
				rename( image_filepath, path.join(dump_directory, path.basename(image_filepath)) )
				break
		# if it is *not* similar to any other images, add to the active_cache
		if not isSimilar:
			active_cache[image_filepath] = hash_1
		count += 1

MoveSimilarImagesToDirectory( "E:\\neural\\TO_SORT", "E:\\neural\\TO_SORT\\dump", similarity=98, hash_size=8)
