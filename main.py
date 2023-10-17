# very handy that there is a library for this
from wallpaper import get_wallpaper, set_wallpaper

import requests # for downloading the timetable and etc
from time import sleep # for sleeping
import icalendar # for parsing the timetable

import config # not a very good way to do it, but it works

# check the config
if config.ttURL == None:
	raise Exception("No timetable URL set in config.py (see the README for help!)")

# extra conf stuff but the user won't need to mess with it
staffJson = "https://soc.port.ac.uk/staff/soc.json"
tempFolder = "tmp/"

ttUpdate = 60 * 60 # 1 hour, in seconds
bgUpdate = 60 * 1 # 1 minute, in seconds

# checks whether there is a current event
# if there is, the wallpaper is updated accordingly
def updateBackground():
	
	pass

# this updates the local copy of the timetable/staff list
def downloadTT():
	# download the timetable and save it
	
	# TODO: check if the local copies is different
	# and dont redownload if it's the same
	print("Downloading timetable")
	ttResp = requests.get(config.ttURL)

	with open(f"{tempFolder}tt.ical", "w") as f:
		print("Saving timetable")
		f.write(ttResp.text)
		f.close()
	
	print("Downloading staff list")
	staffResp = requests.get(staffJson)
	with open(f"{tempFolder}staff.json", "w") as f:
		print("Saving staff list")
		f.write(staffResp.text)
		f.close()

def main():
	# TODO: run on a loop and update
	# every hour or so
	downloadTT()
	
	while True:
		updateBackground()
		sleep(bgUpdate)

main()