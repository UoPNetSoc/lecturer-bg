# adds the two VBS scripts to the windows task scheduler
# requires powershell 3 because of $PSScriptRoot, otherwise replace with the full path yourself

1..2 | ForEach-Object {
	if ($_ -eq 1) {
        $arg = "set"
		$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval ([TimeSpan]::FromMinutes(5))
	}
    elseif ($_ -eq 2) {
		$arg = "update"

		$triggerDaily = New-ScheduledTaskTrigger -Daily -At "09:00 AM"
		$triggerAtStartup = New-ScheduledTaskTrigger -AtStartup
		$trigger = @($triggerAtStartup, $triggerDaily)
	}
	
	# run the epic vbs scripts
	$action = New-ScheduledTaskAction -Execute "$PSScriptRoot$arg.vbs"
	
	$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
	$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

	Register-ScheduledTask -force -Action $action -Trigger $trigger -TaskPath "LecturerBG" -TaskName "Lecturer BG $arg" -Principal $principal -Settings $settings
}