# Lecturer Background
Set your computer wallpaper to your current lecturer, according to your timetable (for the UoP School of Computing) 

## Requirements
- `requests`
- `py-wallpaper`


## Config
`config.py` should look like the following:
```python
# tt_url should be set to the ical url of your timetable
tt_url = "http://timetable.myport.ac.uk/123456789ABCD.ics"
```

## Finding the iCal Link
1. Visit [this page](https://portal.myport.ac.uk/student/google-calendar/), and copy the link address of the "Add to Google Calendar" image. 
2. You will have a URL that looks like this: `https://calendar.google.com/render?cid=http://timetable.myport.ac.uk/123456789ABCD.ics`
3. You should remove everything before `http://timetable.myport...`, so you end up with the URL `http://timetable.myport.ac.uk/123456789ABCD.ics`.