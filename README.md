# Lecturer Background
Set your computer wallpaper to your current lecturer, according to your timetable (for the UoP School of Computing) 

Sorry about the code quality. This was written in the space of a few hours, written between lectures (definitely not during...).

## Requirements
```
pip install -r requirements.txt
```

## Config
`config.py` should look like the following:
```python
# ttURL should be set to the ical url of your timetable
ttURL = "http://timetable.myport.ac.uk/123456789ABCD.ics"

# This is the wallpaper to show when there is nothing happening
# Should be placed in the same directory as the script
defaultWallpaper = "default.jpg"

# This is the wallpaper to show when there is something happening,
# but we couldn't find an image for the lecturer
# Should be placed in the same directory as the script
missingWallpaper = "unknown.jpg"
```

## Finding the iCal Link
1. Visit [this page](https://portal.myport.ac.uk/student/google-calendar/), and copy the link address of the "Add to Google Calendar" image. 
2. You will have a URL that looks like this: `https://calendar.google.com/render?cid=http://timetable.myport.ac.uk/123456789ABCD.ics`
3. You should remove everything before `http://timetable.myport...`, so you end up with the URL `http://timetable.myport.ac.uk/123456789ABCD.ics`.

# Running the script
To run the script, it is recommended to add tasks to the Windows Task Scheduler. There should be two tasks.

One that calls the script with the argument of `update` (`python main.py update`), which will update the timetable and staff list - this should be run - this shouldn't need to be run very often.

The other should call the script with the argument of `set` (`python main.py set`), which will set to the current lecturer, or the default if there is no lecturer - this should be run every few minutes (or as frequently as you like) to keep the wallpaper up to date.

# ToDo:
See GitHub Issues for list of things to do.