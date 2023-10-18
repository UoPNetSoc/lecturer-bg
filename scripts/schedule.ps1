# adds the two VBS scripts to the windows task scheduler
# requires powershell 3 because of $PSScriptRoot, otherwise replace with the full path yourself

1..2 | ForEach-Object {
	if ($_ -eq 1) {
        $arg = "set"
		# we can run this hourly, since lectures can only start and finish on the hour
		# im not sure how this will work with the repetition interval, and when during the hour it will run
		$triggerHourly = New-ScheduledTaskTrigger -Once -At "08:00:05" -RepetitionInterval ([TimeSpan]::FromHours(1))
		$triggerAtStartup = New-ScheduledTaskTrigger -AtStartup
		$trigger = @($triggerAtStartup, $triggerHourly)
	}
    elseif ($_ -eq 2) {
		$arg = "update"

		$triggerDaily = New-ScheduledTaskTrigger -Daily -At "09:00 AM"
		$triggerAtStartup = New-ScheduledTaskTrigger -AtStartup
		$trigger = @($triggerAtStartup, $triggerDaily)
	}
	
	# run the epic vbs scripts
	$action = New-ScheduledTaskAction -Execute "$PSScriptRoot\$arg.vbs"
	
	$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
	$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

	Register-ScheduledTask -force -Action $action -Trigger $trigger -TaskPath "LecturerBG" -TaskName "Lecturer BG $arg" -Principal $principal -Settings $settings
}