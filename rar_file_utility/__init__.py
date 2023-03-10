
from shutil import make_archive, rmtree
from os import path, listdir, makedirs, environ, chdir, getcwd, remove

DIRECTORY = path.dirname(path.realpath(__file__))
environ.setdefault("UNRAR_LIB_PATH", path.join(DIRECTORY, "UnRAR64.dll"))

from unrar import rarfile

def _get_replacement_dest_dir(filepath : str) -> str:
	filename, ext = path.splitext( filepath )
	return path.join( path.dirname( filepath ), filename)

def _get_replacement_dest_filepath(filepath : str, extension=None) -> str:
	filename, ext = path.splitext( filepath )
	if extension == None:
		extension = ext
	return path.join( path.dirname( filepath ), filename + extension)

def ExtractRarToDirectory(filepath : str, password=None, dest_dir=None) -> str:
	# default output directoryath: filepath final directory + filename
	if dest_dir == None:
		dest_dir = _get_replacement_dest_dir(filepath)
	with rarfile.RarFile(filepath, 'r', pwd=password) as myrar:
		myrar.extractall(path=dest_dir, pwd=password)
	return dest_dir

def UnRarDirectoryWithPassword(directory : str, password=None, dest_dir=None) -> list[str]:
	directories = [ ]
	for filename in listdir( directory ):
		filepath = path.join(directory, filename)
		out_directory = ExtractRarToDirectory(filepath, password=password, dest_dir=dest_dir)
		directories.append(out_directory)
	return directories

def UnRarDirectoryWithPasswordDict(directory : str, filename_to_pass : dict[str : str], dest_dir=None) -> list[str]:
	directories = [ ]
	for filename, passw in filename_to_pass.items():
		filepath = path.join(directory, filename)
		out_directory = ExtractRarToDirectory(filepath, password=passw, dest_dir=dest_dir)
		directories.append(out_directory)
	return directories

def ConvertRARToZip( rar_filepath : str, zip_filepath : str, password=None, deleteRAR=False ) -> str:
	# if the filepath is not specified, create it based on the directory and filename
	if zip_filepath == None:
		zip_filepath = _get_replacement_dest_filepath(rar_filepath, ".zip")
	# get the temporary working directory for unpacking files
	TEMP_DIRECTORY = path.join( path.dirname( rar_filepath ), "temporary" )
	# make the directory if missing
	makedirs(TEMP_DIRECTORY, exist_ok=True)
	# extract rar files to the directory
	ExtractRarToDirectory(rar_filepath, password, TEMP_DIRECTORY)
	# set working directory to the zip_filepath's directory
	old_dir = getcwd()
	chdir(path.dirname(zip_filepath))
	# create the zip archive after setting working directory
	filename, _ = path.splitext( path.basename(rar_filepath) )
	make_archive(filename, 'zip', TEMP_DIRECTORY)
	# reset chdir to previous value
	chdir(path.dirname(old_dir))
	# remove the temporary directory
	rmtree(TEMP_DIRECTORY, ignore_errors=True)
	# if wanted, delete the rar file
	if deleteRAR == True:
		remove(rar_filepath)
	# return the new zip_filepath
	return zip_filepath

def ConvertRARsInDirectoryToZip( directory : str, password=None, deleteRARs=False ) -> list[str]:
	directories = [ ]
	for filename in listdir( directory ):
		filepath = path.join(directory, filename)
		out_directory = ConvertRARToZip(filepath, password=password, deleteRAR=deleteRARs)
		directories.append(out_directory)
	return directories

def ConvertRARPassDictInDirectoryToZip(directory : str, filename_to_pass : dict[str : str], dest_dir=None) -> list[str]:
	directories = [ ]
	for filename, passw in filename_to_pass.items():
		filepath = path.join(directory, filename)
		out_directory = ConvertRARToZip(filepath, password=passw, dest_dir=dest_dir)
		directories.append(out_directory)
	return directories

if __name__ == '__main__':
	basepath = "C:\\Users\\Declan\\Documents\\"
	rarname = "HG1211 [Thomas Taihei].rar"
	zipname = "HG1211 [Thomas Taihei].zip"
	ConvertRARToZip( path.join(basepath, rarname), path.join(basepath, zipname) , password="Thomas@Taihei")
