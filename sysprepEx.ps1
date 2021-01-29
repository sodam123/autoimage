$spath = "C:\Windows\System32\Sysprep\unattend.xml"
#Start-Process -FilePath C:\Windows\System32\Sysprep\Sysprep.exe -ArgumentList /oobe /generalize /quit /unattend:unattend.xml

C:\Windows\System32\Sysprep\Sysprep.exe /generalize /oobe /quit /unattend:$spath