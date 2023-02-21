from os import rmdir, path
from shutil import rmtree
from find_clone_images import assort_descendants as duple_image_check
from correct_duplicate_names import assort_descendants as dupe_name_check
from compress_images import assort_descendants as compress_descendants
from sort_directory_by_file_type import SortByFileType

# the directory to search
print("Input the filepath to search for cloned images under.")
search_directory = input()

# clone images folder
print("Removing duplicate descendant images!")
clone_directory_name = "clones"
clone_dir_path = path.join(search_directory, clone_directory_name)

# move dupe images to the folder
duple_image_check(search_directory, clone_dir_path)

# delete the folder containing them all
rmtree(clone_dir_path)

# make sure all remaining images have a unique name in this new folder
print("Uniquely identifying descendant images!")
unique_name = "unique_name"
unique_directory = path.join(search_directory, unique_name)
dupe_name_check( search_directory, unique_directory )

# compress all the images in the folder to another
print("Compressing descendant images!")
compressed_name = "compressed"
compressed_directory = path.join(search_directory, compressed_name)
compress_descendants( unique_directory, compressed_directory )

# clear old sort from clone image check
rmtree(unique_directory)

# separate into folders by filetype in the compressed folder
print("Sorting by file-type.")
SortByFileType(compressed_directory)

print("Done!")

# C:\\Users\\Declan\\Pictures
