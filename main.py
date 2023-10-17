# very handy that there is a library for this
from wallpaper import get_wallpaper, set_wallpaper

import requests # for downloading the timetable and etc
from time import sleep # for sleeping

import config # not a very good way to do it, but it works

# check the config
if config.tt_url == None:
	raise Exception("No timetable URL set in config.py (see the README for help!)")

# extra conf stuff but the user won't need to mess with it
staff_json = "https://soc.port.ac.uk/staff/soc.json"
temp_folder = "tmp/"

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
	ttResp = requests.get(config.tt_url)

	with open(f"{temp_folder}tt.ical", "w") as f:
		print("Saving timetable")
		f.write(ttResp.text)
		f.close()
	
	print("Downloading staff list")
	staffResp = requests.get(staff_json)
	with open(f"{temp_folder}staff.json", "w") as f:
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