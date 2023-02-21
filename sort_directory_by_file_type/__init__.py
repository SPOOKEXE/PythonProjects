from os import path, makedirs, listdir
from shutil import move as shu_move

def SortByFileType(dir):
	list_ = listdir(dir)
	for file_ in list_:
		_, ext = path.splitext(file_)
		ext = ext[1:]
		if ext == '': 
			continue
		if path.exists(dir+'/'+ext): 
			shu_move(dir+'/'+file_, dir+'/'+ext+'/'+file_)
		else: 
			makedirs(dir+'/'+ext) 
			shu_move(dir+'/'+file_, dir+'/'+ext+'/'+file_)

if __name__ == '__main__':
	SortByFileType(input("Enter the directory path you would like to sort by file types."))
