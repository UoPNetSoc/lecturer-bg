# very handy that there is a library for this
from wallpaper import get_wallpaper, set_wallpaper

# not a very good way but it works
import config

# check the config
if config.tt_url == None:
	raise Exception("No timetable URL set in config.py (see the README for help!)")

staff_json = "https://soc.port.ac.uk/staff/soc.json"

# this loop is called regularly to check the timetable
def loop():
	# todo: the actual code (lol)