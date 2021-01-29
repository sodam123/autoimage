$adapters=(gwmi win32_networkadapterconfiguration )
Foreach ($adapter in $adapters){
  Write-Host $adapter
  $adapter.settcpipnetbios(2)
}