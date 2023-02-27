from os import path, walk, startfile, makedirs
from shutil import copy as shutil_copy
from tkinter import filedialog as fd

def DoesFileHaveSuffix(file : str, suffix_list : list[str]):
	for suffix in suffix_list:
		if file.endswith(suffix):
			return True
	return False

def ScanRecursivelyForFiles(rootPath, suffix_list):
	items = []
	for root, dirs, files in walk(rootPath):
		for file in files:
			if DoesFileHaveSuffix(file, suffix_list):
				items.append(path.join(root, file))
	return items

def AskForFileSuffixes() -> list[str]:
	filetypes = []
	while True:
		print(filetypes)
		print("Input target suffixes (.png , .mp4 , etc) | 'del' - delete latest | 'done' - move on. ")
		out = input("")
		if out == 'del':
			filetypes.pop()
		elif out == 'done':
			break
		elif out.count('.') == 1 and out.startswith('.'):
			filetypes.append(out)
		else:
			print("invalid suffix given, include the . for the filetype as well")

	return filetypes

script_dir = path.dirname(path.abspath(__file__))
dest_dir = path.join(script_dir, 'resources')
try:
	makedirs(dest_dir)
except OSError:
	pass # already exists

while True:
	if input("Type 'open' to choose a directory. Program will close otherwise. ") == "open":
		image_suffixes = AskForFileSuffixes()
		folderpath = fd.askdirectory()
		print("Scanning for ", image_suffixes, " in ", folderpath)
		foundFiles : list[str] = ScanRecursivelyForFiles(folderpath, image_suffixes)
		print(len(foundFiles), foundFiles)
		i = 0
		for abspath in foundFiles:
			i += 1
			_, tail = path.split(abspath)
			_, ext = path.splitext(tail)
			shutil_copy(abspath, path.join(dest_dir, str(i) + "_" + ext))
		startfile(dest_dir)
	else:
		break
