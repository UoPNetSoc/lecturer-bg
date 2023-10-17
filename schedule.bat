@REM Will schedule running the Python script every so often
@REM /np means that it will not store the password, so you will prob need to run this as an administrator

@REM Current directory:
set programPath=%~dp0
set script=%programPath%bg.ps1

@REM Checks and sets the background every 5 minutes
schtasks /create /np /sc minute /mo 5 /tn "Lecturer BG Set" /tr "%script% set"

@REM Update daily
schtasks /create /np /sc daily /tn "Lecturer BG Update" /tr "%script% update"