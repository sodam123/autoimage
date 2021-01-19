@echo off
color 0a
mode 1000
 
:a
 
$adapters=(gwmi win32_networkadapterconfiguration )
Foreach ($adapter in $adapters){
  Write-Host $adapter
  $adapter.settcpipnetbios(1)
}

ping > nul
ping > nul
ping > nul
 
goto a