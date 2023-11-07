# Lecturer Background
# https://github.com/UoPNetSoc/lecturer-bg
# By TomR.me, JackConnolly.net (NetSoc.group), 2023

# To any lecturers who may be looking at this code: sorry. You should probably stop reading now.
# This is the epitome of bodge. Made in a few hours and then perpetually added to over time.
# We care more about our code quality in our uni work, don't worry!
# Somehow everything mostly works though, which is honestly a miracle.
# - Tom

from time import sleep # for sleeping
from datetime import datetime # for checking the time
from pytz import utc # for timezone stuff
import requests # for downloading the timetable and etc
import urllib3 # for downloading the timetable and etc
import ssl # for downloading the timetable and etc
import icalendar # for parsing the timetable
import recurring_ical_events # new timetable system brokey
import json # for parsing the staff list
import ctypes # for setting the wallpaper
import os # for getting the full path of the image
import sys # for getting the arguments
import random # for choosing random images

# for funny image manipulation
from PIL import Image, ImageFilter
import pillow_avif

import config # not a very good way to do it, but it works

# extra conf stuff but the user won't need to mess with it
staffJson = "https://soc.port.ac.uk/staff/soc.json"
currentFolder = os.path.abspath(os.path.dirname(__file__))
tempFolder = f"{currentFolder}\\tmp\\"

# set these to true to test the wallpaper, SHOULD always set the wallpaper to the respective person
# will only work for those on the networking course
# for testing and debugging purposes only, make sure to set to false before committing(hi its jack i've committed while true wayy too many times)
# sorry tom
# sorry tom
# sorry tom
# sorry tom
# this code really is a mess
rinatTime = False
nadimTime = False

def main():
	# get arguments
	firstArg = None
	try:
		firstArg = sys.argv[1]
	except IndexError:
		print("No arguments! Please see the README for help on how to run.")
		sys.exit()

	# python doesnt have nice switch statements :(

	if firstArg == "update":
		fetchAndSave()
	elif firstArg == "set":
		updateBackground()
	else:
		print(f"Unrecognised argument '{firstArg}', please see the README for help on how to run.")
#yandere dev ^^^
# check the config
def checkConfig():
	if config.ttURL == None:
		raise Exception("No timetable URL set in config.py (see the README for help!)")

	if config.defaultWallpaper == None:
		raise Exception("No default wallpaper set in config.py (see the README for help!)")

	if config.missingWallpaper == None:
		raise Exception("No missing wallpaper set in config.py (see the README for help!)")

# checks whether there is a current event
# if there is, the wallpaper is updated accordingly
def updateBackground():
	# check if the files exists
	# if it doesn't, then download them
	try:
		with open(f"{tempFolder}tt.ics") as f:
			f.close()

		with open(f"{tempFolder}staff.json") as f:
			f.close()
	except FileNotFoundError:
		fetchAndSave()

	try:
		with open(f"{tempFolder}tt.ics") as f:
			f.close()
	except FileNotFoundError:
		return print("Missing timetable...")

	# open the files and parse them
	with open(f"{tempFolder}tt.ics") as f:
		cal = icalendar.Calendar.from_ical(f.read())
		f.close()

	now = datetime.now()

	if rinatTime == True:
		now = datetime(2023, 10, 16, 17, 0, 0) # fixed time for testing

	if nadimTime == True:
		now = datetime(2023, 11, 7, 14, 15, 25)
	
	now = now.astimezone()

	nowEvents = recurring_ical_events.of(cal).at(now)

	for event in nowEvents:
		title = event.get('summary')
		startTime = event.get('dtstart').dt
		endTime = event.get('dtend').dt
		notes = event.get('description')

		print(f"Current event: {title} ({startTime} - {endTime})")
		print(f"Notes: {notes}")
		
		# TODO: NEW UOP TIMETABLING SYSTEM
		# SEE ISSUE #9

		lines = notes.split("\n")
		
		lastLine = lines[-2] # for some reason the last line is always blank so get second last

		print(f"Last line: {lastLine}")

		# if contains a comma then we will assume it's a lecturer
		# example: Bakhshov, Nadim, Boakes, Rich
		# we will go based on the first lecturer in the list, so 0 and 1 when split(", ")
		# TODO: we could make a fun grid of multiple lecturers?
					
		if "," in lastLine:
			split = lastLine.split(", ")
			firstName = split[1].replace(" ", "")
			lastName = split[0].replace(" ", "")
			print(f"Found lecturer, hopefully: {firstName} {lastName}")
		else:
			print("Couldn't find lecturer in notes :(")
			setMissingWallpaper()
			return

		# find the staff member's image
		imageName, imageURL = findStaffMemberImageURL(f"{firstName} {lastName}")
		# "imageName" ends up as the staff member's name, which is used as the folder name	

		if imageName == None:
			print("Couldn't find staff member in staff list :(")
			setMissingWallpaper()
			return
		# else:


		# where we will store images
		imagePath = f"{tempFolder}images/{imageName}"

		if not os.path.exists(imagePath):
			os.makedirs(imagePath)

		# check if the image from the staff board already exists
		if os.path.isfile(f"{imagePath}/{imageName}.avif"):
			print(f"Image {imageName} already downloaded")
		else:
			# if it doesn't, we download it
			print("Downloading image")
			imageResp = contentReq(imageURL)
			with open(f"{imagePath}/{imageName}.avif", "wb") as f:
				f.write(imageResp.content)
				f.close()

		# magic from https://stackoverflow.com/a/3207973
		# gets the list of filenames in the folder
		filenames = next(os.walk(imagePath), (None, None, []))[2]
		# remove filenames that end with "-stretch.jpg" (thanks copilot)
		filenames = [f for f in filenames if not f.endswith("-stretch.jpg")]

		# pick random filename from the folder
		image = random.choice(filenames)
	
		# set the wallpaper
		# full path of the image is needed
		fullPath = os.path.abspath(f"{tempFolder}images/{imageName}/{image}")

		# "fix" is a bit of a stretch
		fixedImagePath = fixImageAndGetPath(fullPath)

		setWallpaper(fixedImagePath, True)

		# for some reason it sometimes gives multiple events at once?
		# this is a janky fix for that, so it only does the first one
		return
		
	# if we get here, then there is no current event
	# so we set the default wallpaper
	print("No current event, setting default wallpaper")
	setDefaultWallpaper()

# this updates the local copy of the timetable/staff list
def fetchAndSave():
	# download the timetable and save it
	
	# TODO: check if the local copies is different
	# and dont redownload if it's the same
	print("Downloading timetable")
	tt = textReq(config.ttURL)

	# arbi
	if(len(tt) < 10):
		print("Timetable body was empty. Sometimes it breaks, so maybe try again later?")
		print(f"You can also visit the iCal file in your browser and save it to {tempFolder}tt.ics")
		print("If you have already done that, you can ignore this message")
		print(config.ttURL)
	else:
		with open(f"{tempFolder}tt.ics", "w") as f:
			print("Saving timetable")
			f.write(tt)
			f.close()
		
	print("Downloading staff list")
	staffResp = jsonReq(staffJson)

	# there are three sections to the staff json: heads, professors, and staff
	# we will combine them here
	print("Parsing staff list")
	staffList = []
	for s in staffResp["heads"]:
		staffList.append(s)
	for s in staffResp["professors"]:
		staffList.append(s)
	for s in staffResp["staff"]:
		staffList.append(s)

	with open(f"{tempFolder}staff.json", "w") as f:
		print("Saving staff list")
		f.write(json.dumps(staffList))
		f.close()

# find the staff member in the list and return their image
def findStaffMemberImageURL(name):
	# does the staff list file exist?
	try:
		with open(f"{tempFolder}staff.json") as f:
			f.close()
	except FileNotFoundError:
		fetchAndSave()

	with open(f"{tempFolder}staff.json") as f:
		staffJson = json.loads(f.read())
		f.close()

	name = name.lower().replace("dr ", "")

	# find the staff member in the list
	for s in staffJson:
		sName = s.get("name").lower().replace("dr ", "")
		
		if(sName == name):
			# we have found our staff member, get their images
			images = s.get("images")
			
			if images == None:
				return None
			
			# get the first image
			image = images[0] # is just the staff member's name
			imageURL = f"https://soc.port.ac.uk/staff/pix/{image}/{image}.avif"
			return(image, imageURL)
		
	# if we get here, then we haven't found the staff member
	return None


# actually sets the wallpaper using beautiful windows APIs
def setWallpaper(filePath, stretch=False):
	print(f"Setting wallpaper to {filePath}, stretch={stretch}")

	# this seems to not actually work, but it's here anyway
	# i love windows
	if stretch:
		# stretch is 1
		style = 1
	else:
		# fill is 10?
		style = 10

	ctypes.windll.user32.SystemParametersInfoW(20, 0, filePath, style)

def setDefaultWallpaper():
	fullPath = f"{currentFolder}\\{config.defaultWallpaper}"
	setWallpaper(fullPath)

def setMissingWallpaper():
	fullPath = f"{currentFolder}\\{config.missingWallpaper}"
	setWallpaper(fullPath, True)

# beautifully named function
# (it stretches the image to the screen resolution, and then saves it as a jpg)
# returns the path to the new jpg
def fixImageAndGetPath(imgPath):
	newPath = f"{imgPath}-stretch.jpg"

	# if already exists, return it
	if os.path.exists(newPath):
		print(f"Image already fixed up, returning {newPath}")
		return newPath

	print(f"Fixing up {imgPath} with pillow")
	
	# get the screen resolution, and divide by 2
	screenWidth = ctypes.windll.user32.GetSystemMetrics(0) // 2
	screenHeight = ctypes.windll.user32.GetSystemMetrics(1) // 2
	
	# load the image
	img = Image.open(imgPath)
	# resize it to the screen resolution, and convert it to RGB
	img = img.resize((screenWidth, screenHeight)).convert("RGB")

	# save as jpg with 10% quality :)
	img.save(newPath, quality=10)

	return newPath



# these are just wrappers for the requests library
# they disable SSL verification because that broke on jack's laptop
def textReq(url):
	# return a text response from a url
	return get_legacy_session().get(url).text

def contentReq(url):
	# return a content response from a url
	return get_legacy_session().get(url)

def jsonReq(url):
	# return a json response from a url
	return json.loads(textReq(url))

# make the temp folders if they don't exist
def makeTempFolders():
	if not os.path.exists(tempFolder):
		os.makedirs(tempFolder)
	if not os.path.exists(f"{tempFolder}images"):
		os.makedirs(f"{tempFolder}images")

# This random code is from https://stackoverflow.com/a/73519818
# Fixes Jack's issue (#6), but really shouldn't be neccesary
class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

def get_legacy_session():
	ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
	ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT

	session = requests.session()
	session.headers = {
		'User-Agent': 'Lecturer BG (+https://github.com/UoPNetSoc/lecturer-bg)'
	}
	session.mount('https://', CustomHttpAdapter(ctx))
	return session

if __name__ == "__main__":
	checkConfig()
	makeTempFolders()
	main()