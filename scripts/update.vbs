' ChatGPT suggested this method to run the script in the background, it's quite funny
' what even is this language

' What is this absolute witchcraft??
Dim goFS  : Set goFS  = Createobject("Scripting.FileSystemObject")


' two levels up from the current script is where main.py should be
path = goFS.GetParentFolderName(goFS.GetParentFolderName(WScript.ScriptFullName))
path = path & "\main.py"

command = "pythonw.exe " & path & " update"

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run command, 0