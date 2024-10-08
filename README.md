# Lecturer Background

> **⚠️ This no longer works :(**
>   
> This project was designed to use an older version of the University's timetabling system, and an older version of the School of Computing's staff board website. It is unlikely that we will update the project to support the changes, however you are welcome to create forks. If anything changes and we find the time, maybe this repo will be come back from the dead.  
>   
> Here is a [▶️ video](https://youtu.be/oufEE-sbeVY) showing LecturerBG in its finest hour, reminding us that we were late for a lecture from Farzad :(
>   
> So long, and thanks for all the 'why you stretch my face.' 🫡

![A photograph of a laptop, with the desktop wallpaper set to a stretched photograph of a Russian tutor in a white shirt](https://github.com/UoPNetSoc/lecturer-bg/assets/14424577/5967b58f-aaab-4ef1-ab80-12dfd76a208e)

Set your computer wallpaper to your current lecturer, according to your timetable (only works for the UoP School of Computing).

Please don't look at the code... it's baaaaad. Sorry. Everything is a bodge. This was originally hacked together between lectures (def not during), and has been patched and added to ever since. Sorry, again, Nadim, we love you.

Everything should be treated as WIP, and we're not responsible if this does anything bad to your poor computer. Only works on Windows, but there are probably easy ways to port it to macOS/Linux DEs. Please don't beg us for support, if you're nerdy enough to use this, you can probably try and fix any issues.

The photographs of lecturers are systematically organized into dedicated folders within the temporary directory. Should you desire to include your own images of these individuals, you can you can place them in the appropriate folder (`tmp/images/LECTURER NAME/`). They will be randomly selected when the script is run.

# Installation
## Requirements
```
pip install -r requirements.txt
```

## Config
`config.py` should look like the following:
```python
# ttURL should be set to the ical url of your timetable
# see the README if you need help obtaining this
ttURL = "https://timetabling.port.ac.uk/iCal/[random string]/calendar.ics"

# This is the wallpaper to show when there is nothing happening
# Should be placed in the same directory as the script
defaultWallpaper = "default.jpg"

# This is the wallpaper to show when there is something happening,
# but we couldn't find an image for the lecturer
# Should be placed in the same directory as the script
missingWallpaper = "unknown.jpg"
```

### Finding the iCal Link
1. Visit CMISGo, the University's timetabling system at [timetabling.port.ac.uk](https://timetabling.port.ac.uk/Web/Timetable)
2. Select "Administration" and then "My mobile" in the menu in the top right
3. In the popup, there will be an option to set up access from a mobile device calendar, using the "Create link" button.
4. This is the link you need to insert into the config! _You can also use this link to subscribe to your timetable in any calendaring app, such as an app on your phone!_

### A note on the Timetable
Sometimes CMISGo breaks and the program will fail download the timetable calendar file. In this case, you can download it manually and save it to `tmp/tt.ics`. This is a pain, but I don't think it's the fault of the program. It worked fine with the old timetable system.

# Running the Script
To run the script, it is easiest to add tasks to the Windows Task Scheduler. There should be two tasks, one that runs `main.py set` to update the wallpaper, and another that runs `main.py update` that periodically updates the local copy of the staff list and timetable.

There is a [PowerShell script](scripts/schedule.ps1) that will create the tasks for you (needs to be ran as admin I think). The beautiful VBScript files ensure that the program runs without a console window visible. It was ChatGPT's idea, so don't blame me.

The first time you run the script, you should do it manually and check the console output for problems. Please open a GitHub issue if you encounter anything weird. This is very hacky and terrible, so things will probably not work first-try for everyone.

# To Dos:
See GitHub Issues for list of things to do.


# Fun Quotes from Lecturers
*"A little bit weird but quite cool - I need to have a more stern expression"* - Rinat

*"You make me laugh! I dont mind."* - Linda

*"-picks up laptop and shows the class- This is an example of inappropriate lab behaviour"* - Vas

*"-laughs hysterically and slaps Jack on the back- Would you like more photos? I can send more photos, send me an email"* - Farzad

*"That's great! You could sell that back to the School!"* - Nadim

*"This is a flagrant abuse of copyright law, a misuse of university intellectual property and is almost certainly covered by the uni's computer misuse policy, so you should **probably** make it a private repo - this doesn't mean it's not staggeringly funny, but cover your ass"* - Rich (if anyone has a problem with this - bear in mind we are not distributing any copyrighted material ourselves - we will be nice and private this repo, just let us know)

# Contributers
- This is the brainchild of the almighty Jack, ([@jdc0101](https://github.com/jdc0101)) (taking the role of Steve Jobs) (he did help tho with some of it(its a team effort))
- Tom, [@itsmeimtom](https://github.com/itsmeimtom), actually did all the work and wrote the code (taking the role of Steve Wozniak)
- Special thanks to GitHub Copilot, who has these words to say here: *"I'm not sure what to say, but I'm sure you'll be able to find a way to make it work."*
