from sys import exc_info
import re, urllib.request, os
from random import randint

# List of given Urls
galleryList = []
# List of open page sourcecodes
galleryPages = []
# List of image ids found in page sourcecode
imageId = []
# List of open image page sourcecode
imagePage = []
#List of image source urls
imageUrl = []

def getGalleryList():
	global galleryList
	queryGalleryId = re.compile('[0-9]+')
	enter = 0
	print("Enter the Gallery Urls:   (Press Enter TWICE to continue.)")
	while(True):
		choice = str(input())
		if choice == "":
			enter += 1
			if enter == 2:
				break
		else:
			enter = 0
			for ch in choice.split('\n'):
				url = "http://www.imagefap.com/pictures/"
				galleryId = queryGalleryId.findall(ch.strip())[0]
				url = url + galleryId + "/?gid={}&view=2".format(galleryId)
				galleryList.append(url)

def loadGalleryPage():
	global galleryList, galleryPages
	print("Loading Gallery Page")
	
	for page in galleryList:
		try:
			with urllib.request.urlopen(page) as f:
				galleryPages.append(f.read())
		except Exception as e:
			print("Unexpected Error: ", exc_info()[0], e)
			print("Error at loadGalleryPage")

def loadImagePage(pageUrl):
	try:
		with urllib.request.urlopen(pageUrl) as f:
			imagePage = f.read()
			return imagePage
	except Exception as e:
		print("Unexpected Error: ", exc_info()[0], e)
		print("Error at loadGalleryPage")

def getImagesInGallery():
	global imageId, galleryPages
	print("Getting Images In Gallery")
	try:
		for gallery in galleryPages:
			result = re.findall('<td id="([0-9]+)" align="center"  ?valign="top">', str(gallery))
			imageId.extend(result)
		
	except Exception as e:
		print("Unexpected Error: ", exc_info()[0], e)
		print("Error at getImagesInGallery")

def findImageUrl():
	global imageId, imagePage, imageUrl
	print("Finding Image Urls")
	try:
		for picId in imageId:
			imagePage.append(loadImagePage("http://www.imagefap.com/photo/{}/".format(picId)))
		for page in imagePage:
			result = re.findall('"contentUrl": "(.*?)",', str(page))
			imageUrl.append(result[0])
		print("The following files have been queued for download:")
		for url in imageUrl:
			print(url)
	except Exception as e:
		print("Unexpected Error: ", exc_info()[0], e)
		print("Error at findImageUrl")

def downloadImage():
	global imageUrl
	try:
		for image in imageUrl:
			name = image.split("/")[-1]
			dir_name = image.split("/")[-3]
			print("Image Downloading: {}".format(name))
			imageContent = 0
			with urllib.request.urlopen(image) as f:
				imageContent = f.read()
			
			if os.path.isfile(name):
				name = name.rsplit('.', 1)[0] + '_' + str(randint(1111111, 9999999)) + '.' + name.rsplit('.', 1)[1]
			
			try:
				os.mkdir(dir_name)
			except:
				pass
				
			with open(dir_name + '/' + name, "wb") as f:
				f.write(imageContent)
	except Exception as e:
		print("Unexpected Error: ", exc_info()[0], e)
		print("Error at downloadImage")

if __name__=="__main__":
	getGalleryList()
	loadGalleryPage()
	getImagesInGallery()
	findImageUrl()
	downloadImage()
