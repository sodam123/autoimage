$spath = "C:\Windows\System32\Sysprep\unattend.xml"
#Start-Process C:\Windows\System32\Sysprep\Sysprep.exe /oobe /generalize /quit /unattend:+$spath -NoNewWindow -Wait

C:\Windows\System32\Sysprep\Sysprep.exe /generalize /oobe /quit /unattend:$spath | Out-Null