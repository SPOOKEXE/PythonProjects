
from shutil import make_archive, rmtree
from os import path, listdir, makedirs, environ, chdir, getcwd, remove, rename
from concurrent import futures
from typing import Union

DIRECTORY = path.dirname(path.realpath(__file__))
environ.setdefault("UNRAR_LIB_PATH", path.join(DIRECTORY, "UnRAR64.dll"))

from unrar import rarfile

THREAD_POOL = futures.ThreadPoolExecutor(max_workers=30)

def _get_replacement_dest_dir(filepath : str) -> str:
	filename, ext = path.splitext( path.basename(filepath) )
	return path.join( path.dirname( filepath ), filename)

def _get_replacement_dest_filepath(filepath : str, extension=None) -> str:
	filename, ext = path.splitext( path.basename(filepath) )
	if extension == None:
		extension = ext
	return path.join( path.dirname( filepath ), filename + extension)

def ExtractRarToDirectory(filepath : str, password : Union[None, str], dest_dir : Union[None, str]) -> str:
	# default output directoryath: filepath final directory + filename
	if dest_dir == None:
		dest_dir = _get_replacement_dest_dir(filepath)
	with rarfile.RarFile(filepath, 'r', pwd=password) as myrar:
		myrar.extractall(path=dest_dir, pwd=password)
	return dest_dir

def UnRarDirectoryWithPassword(directory : str, password : Union[None, str], dest_dir : Union[None, str]) -> list[str]:
	counter = 0
	promise_array = []
	for filename in listdir(directory):
		if filename.endswith(".rar"):
			filepath = path.join(directory, filename)
			promise = THREAD_POOL.submit( ExtractRarToDirectory, filepath, password, dest_dir )
			promise_array.append(promise)
			counter += 1
	destinations = []
	for promise in futures.as_completed( promise_array ):
		destinations.append( promise.result() )
		counter -= 1
		print("awaiting ", counter, " more threads to finish.")
	return destinations

def ConvertRARToZip( rar_filepath : str, zip_filepath : Union[None, str], password : Union[None, str], deleteRAR : Union[None, bool] ) -> str:
	# if the filepath is not specified, create it based on the directory and filename
	if zip_filepath == None:
		zip_filepath = _get_replacement_dest_filepath(rar_filepath, ".zip")
	
	# if it is already completed
	if path.exists(zip_filepath):
		# if wanted, delete the rar file
		if deleteRAR == True:
			remove(rar_filepath)
		return zip_filepath
	
	# get the temporary working directory for unpacking files
	filename, _ = path.splitext( path.basename(rar_filepath) )
	TEMP_DIRECTORY = path.join( path.dirname( rar_filepath ), filename )
	
	# make the directory if missing
	makedirs(TEMP_DIRECTORY, exist_ok=True)
	
	# extract rar files to the directory
	ExtractRarToDirectory(rar_filepath, password, TEMP_DIRECTORY)
	
	# create the zip archive after setting working directory
	filename, _ = path.splitext( path.basename(rar_filepath) )
	try:
		make_archive( path.join( path.dirname( rar_filepath ), filename ), 'zip', TEMP_DIRECTORY)
	except Exception as e:
		print( filename, " failed to extract\n", e )

	# remove the temporary directory
	rmtree(TEMP_DIRECTORY, ignore_errors=True)
	
	# if wanted, delete the rar file
	if deleteRAR == True:
		remove(rar_filepath)
	
	# return the new zip_filepath
	return zip_filepath

def ConvertRARsInDirectoryToZip( directory : str, password=None, deleteRARs=False ) -> list[str]:
	counter = 0
	promise_array = []
	for filename in listdir(directory):
		if filename.endswith(".rar"):
			filepath = path.join(directory, filename)
			promise = THREAD_POOL.submit( ConvertRARToZip, filepath, None, password, deleteRARs )
			promise_array.append(promise)
			counter += 1
	destinations = []
	for promise in futures.as_completed( promise_array ):
		destinations.append( promise.result() )
		counter -= 1
		print("awaiting ", counter, " more threads to finish.")
	return destinations

if __name__ == '__main__':
	pass # currently a few fileanme errors (and folders in folders causing problems)
	# ConvertRARsInDirectoryToZip("C:\\Users\\Declan\\Documents\\SmallerThan100MB", "Thomas@Taihei", deleteRARs=False)
	# ConvertRARToZip("C:\\Users\\Declan\\Documents\\HG1113_v1.01 [Thomas Taihei].rar", None, "Thomas@Taihei", False)
