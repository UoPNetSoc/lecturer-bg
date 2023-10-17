# Lecturer Wallpaper
# https://github.com/UoPNetSoc/lecturer-bg

from time import sleep # for sleeping
from datetime import datetime # for checking the time
from pytz import utc # for timezone stuff
import requests # for downloading the timetable and etc
import icalendar # for parsing the timetable
import json # for parsing the staff list
import ctypes # for setting the wallpaper
import os # for getting the full path of the image

import config # not a very good way to do it, but it works

# check the config
if config.ttURL == None:
	raise Exception("No timetable URL set in config.py (see the README for help!)")

if config.defaultWallpaper == None:
	raise Exception("No default wallpaper set in config.py (see the README for help!)")

if config.missingWallpaper == None:
	raise Exception("No missing wallpaper set in config.py (see the README for help!)")

# extra conf stuff but the user won't need to mess with it
staffJson = "https://soc.port.ac.uk/staff/soc.json"
tempFolder = "tmp/"

ttUpdate = 60 * 60 # 1 hour, in seconds
bgUpdate = 60 * 1 # 1 minute, in seconds

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
		downloadTT()

	# open the files and parse them
	with open(f"{tempFolder}tt.ics") as f:
		calendar = icalendar.Calendar.from_ical(f.read())
		f.close()

	with open(f"{tempFolder}staff.json") as f:
		staffJson = json.loads(f.read())
		f.close()

	for event in calendar.walk('VEVENT'):
		title = event.get('summary')
		startTime = event.get('dtstart').dt
		endTime = event.get('dtend').dt
		notes = event.get('description')

		# check if the event is happening now
		now = datetime.now()

		# now = datetime(2023, 10, 17, 11, 0, 0) # fixed time for testing
		
		# make now aware of the timezone
		now = utc.localize(now)
		# convert the event times to UTC
		startTime = startTime.astimezone(utc)
		endTime = endTime.astimezone(utc)

		if startTime <= now <= endTime:
			# this event is happening now!

			print(f"Current event: {title} ({startTime} - {endTime})")
			print(f"Notes: {notes}")
			
			# find the string that contains lecturer
			lecturer = None
			for line in notes.split("\n"):
				if "lecturer" in line.lower():
					lecturer = line.split(": ")[1]
					break
			
			if lecturer == None:
				print("Couldn't find lecturer in notes")
				# TODO: set default wallpaper if no lecturer is found, or no event
				return
			
			firstName = lecturer.split(", ")[1]
			lastName = lecturer.split(", ")[0]

			
			# find the staff member in the list
			for s in staffJson:
				ourName = f"{firstName} {lastName}".lower()
				name = s.get("name").lower().replace("dr ", "").replace("prof ", "")
				
				print(f"Checking '{name}' against '{ourName}'")

				if(name == ourName):
					# we have found our staff member, get their images
					images = s.get("images")
					
					if images == None:
						print("No images found for this staff member, setting missing wallpaper")
						setMissingWallpaper()
						return # we don't need to do anything else
					
					# get the first image
					image = images[0] # is just the staff member's name
					imageURL = f"https://soc.port.ac.uk/staff/pix/{image}/{image}.avif"
					print(imageURL)

					# check if the image is already downloaded
					# if it is, then we don't need to download it again

					if os.path.isfile(f"{tempFolder}staff/{image}.avif"):
						print("Image already downloaded")
					else:
						# download the image
						print("Downloading image")
						imageResp = contentReq(imageURL)
						with open(f"{tempFolder}staff/{image}.avif", "wb") as f:
							f.write(imageResp.content)
							f.close()
				
					# set the wallpaper
					# full path of the image is needed
					print("Setting wallpaper")
					fullPath = os.path.abspath(f"{tempFolder}staff/{image}.avif")
					setWallpaper(fullPath, True)

					return # done

			# for some reason it sometimes gives multiple events at once?
			# this is a janky fix for that, so it only does the first one
			return
		
	# if we get here, then there is no current event
	# so we set the default wallpaper
	print("No current event, setting default wallpaper")
	setDefaultWallpaper()

# this updates the local copy of the timetable/staff list
def downloadTT():
	# download the timetable and save it
	
	# TODO: check if the local copies is different
	# and dont redownload if it's the same
	print("Downloading timetable")
	tt = textReq(config.ttURL)

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

def setWallpaper(filePath, stretch=False):
	print(f"Setting wallpaper to {filePath}, stretch={stretch}")

	if stretch:
		# stretch is 1
		style = 1
	else:
		# fill is 10?
		style = 10

	ctypes.windll.user32.SystemParametersInfoW(20, 0, filePath, style)

def setDefaultWallpaper():
	fullPath = os.path.abspath(config.defaultWallpaper)
	setWallpaper(fullPath)

def setMissingWallpaper():
	fullPath = os.path.abspath(config.missingWallpaper)
	setWallpaper(fullPath, True)

# these are just wrappers for the requests library
# they disable SSL verification because that broke on jack's laptop
def textReq(url):
	# return a text response from a url
	return requests.get(url, verify=False).text

def contentReq(url):
	# return a content response from a url
	return requests.get(url, verify=False).content

def jsonReq(url):
	# return a json response from a url
	return json.loads(textReq(url))

def main():
	# create temp folders
	if not os.path.exists(tempFolder):
		os.makedirs(tempFolder)
	if not os.path.exists(f"{tempFolder}staff"):
		os.makedirs(f"{tempFolder}staff")
		

	# TODO: run on a loop and update
	# every hour or so
	downloadTT()
	
	while True:
		updateBackground()
		sleep(bgUpdate)

	# setMissingWallpaper()

main()