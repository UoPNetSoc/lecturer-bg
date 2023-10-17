# This is a PowerShell script that will launch the Python script

$arg = $args[0]

# current directory of this script (thanks copilot)
$scriptpath = $MyInvocation.MyCommand.Path

$script = Split-Path $scriptpath
$script += "\main.py"

Start-Process -WindowStyle Hidden python.exe "$script $arg"
