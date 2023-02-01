import requests

def DownloadIMG( url ):
	response = requests.get(url)
	filename = url[url.rfind("/")+1:len(url)]
	file = open(filename + ".png", "wb")
	file.write(response.content)
	file.close()

while True:
	input_url = input("Enter the URL to the media. Enter 'exit' otherwise.")
	if input_url == "exit":
		break
	try:
		DownloadIMG( input_url )
		print("Downloaded.")
	except:
		print("Could not download from URL. ")
		pass
