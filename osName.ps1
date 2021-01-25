

 $osname = (Get-WmiObject Win32_OperatingSystem).Name.split("|")
 #write-host($osname[0])
 return $osname[0]

