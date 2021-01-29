<#$fpath = "C:\ouput.txt"
netstat -na | Out-File -FilePath $fpath
#rm -force c:\output.txt
$var = Get-Content -path $fpath

FOREACH-Object {Get-Acl $fpath} | Select-Object protocol, localAddr, exAddr, status

write($var)#>

<#function Get-ProcessPorts{
    [cmdletbinding()]
    Param(
       [parameter(Mandatory=$True, ValueFromPipeLine=$True)]
       [AllowEmptyCollection()]
       [string[]]$ProcessName
    )
    Begin{    
        Write-Verbose "Declaring empty array to store the output"
        $portout = @()            
    }
    Process{
         Write-Verbose "Processes to get the port information"      
         $processes = Get-Process $ProcessName  
         foreach($proc in $processes){
              # Get the port for the process.
              $mports = Netstat -ano | findstr $proc.ID
              # Separate each instance
              foreach($sport in $mports){
                  # Split the netstat output and remove empty lines from the output.
                  $out = $sport.Split('') | where{$_ -ne ""}
                  $LCount = $out[1].LastIndexOf(':')
                  $RCount = $out[2].LastIndexOf(':')
                  $portout += [PSCustomObject]@{              
                    'Process'  = $proc.Name
                    'PID' = $proc.ID
                    'Protocol' = $out[0]
                    'LocalAddress' = $out[1].SubString(0,$LCount)
                    'LocalPort' = $out[1].SubString($Lcount+1,($out[1].Length-$Lcount-1))
                    'RemoteAddress' = $out[2].SubString(0,$RCount)
                    'RemotePort' = $out[2].SubString($RCount+1,($out[2].Length-$Rcount-1))
                    'Connection' = $(
                       # Checking if the connection contains any empty string.
                       if(!($out[3] -match '\d')){$out[3]}      
                    )
                 }
              }  
        }
        $portout | ft -AutoSize
     }
     End{
     Write-Verbose "End of the program"
  }
}#>

#$res = netstat -ano | findstr ":445"
$res = Get-NetTCPConnection -State Listen | select-Object -Property LocalAddress,
LocalPort,RemoteAddress,RemotePort,state

foreach($ele in $res){

   if($ele.LocalPort -eq "445"){
      
      $ele.LocalPort
      $netBTParametersPath = "HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters" 
      if(Test-Path -Path $netBTParametersPath) { 
         Set-ItemProperty -Path $netBTParametersPath -Name "SMBDeviceEnabled" -Value 0 
      } 
      Set-Service lanmanserver -StartupType Disabled 
      Stop-Service lanmanserver -Force

   }

}
