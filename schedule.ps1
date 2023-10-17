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

	# run powershell minimized that has a python script as argument
	$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-WindowStyle Minimized -ExecutionPolicy Bypass -Command 'python.exe $script $arg'"
	
	$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
	$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

	Register-ScheduledTask -force -Action $action -Trigger $trigger -TaskName "Lecturer BG $arg" -Principal $principal -Settings $settings
}