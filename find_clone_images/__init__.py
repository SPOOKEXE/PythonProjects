from detect import assort_directory, assort_descendants

if __name__ == '__main__':
	from os import path

	class SwitchCase:
		def default_switch_case_callback():
			pass
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

	menu = SwitchCase()
	menu.Case('1', assort_descendants)
	menu.Case('2', assort_directory)

	# C:\Users\Declan\Pictures

	while True:
		print("Input the filepath to search for clone images under.")
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
