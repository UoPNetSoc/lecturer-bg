# Lecturer Background
Set your computer wallpaper to your current lecturer, according to your timetable (for the UoP School of Computing) 

## Requirements
- `requests`, `time`
- `py-wallpaper`
- `icalendar`

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

# ToDo:
See GitHub Issues for list of things to do.