# Lecturer Background
![A photograph of a laptop, with the desktop wallpaper set to a stretched photograph of a Russian tutor](https://github.com/UoPNetSoc/lecturer-bg/assets/14424577/b616165a-a90c-4f35-a1e3-0dff21971525)

Set your computer wallpaper to your current lecturer, according to your timetable (only works for the UoP School of Computing).

Sorry about the code quality. This was written in the space of a few hours, between lectures (definitely not during...).

Everything should be treated as WIP, and we're not responsible if this does anything bad to your poor computer. Only works on Windows, but there are probably easy ways to port it to macOS/Linux DEs.

# Installation
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

### Finding the iCal Link
1. Visit [this page](https://portal.myport.ac.uk/student/google-calendar/), and copy the link address of the "Add to Google Calendar" image. 
2. You will have a URL that looks like this: `https://calendar.google.com/render?cid=http://timetable.myport.ac.uk/123456789ABCD.ics`
3. You should remove everything before `http://timetable.myport...`, so you end up with the URL `http://timetable.myport.ac.uk/123456789ABCD.ics`.

# Running the Script
To run the script, it is easiest to add tasks to the Windows Task Scheduler. There should be two tasks, one that runs `main.py set` to update the wallpaper, and another that runs `main.py update` that periodically updates the local copy of the staff list and timetable.

There is a [PowerShell script](scripts/schedule.ps1) that will create the tasks for you (needs to be ran as admin I think). The beautiful VBScript files ensure that the program runs without a console window visible. It was ChatGPT's idea, so don't blame me.

# To Dos:
See GitHub Issues for list of things to do.

# Fun Quotes from Lecturers
*"A little bit weird but quite cool - I need to have a more stern expression"* - Rinat
