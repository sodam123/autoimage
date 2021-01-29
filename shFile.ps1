Set-Service -Name "LanmanServer" -StartupType Automatic
Start-Service -Name "LanmanServer"

$share = Get-SmbShare

Foreach($sh in $share){

    if($sh.Name -ne "C$" -and $sh.Name -ne "D$" -and $sh.Name -ne "IPC$" -and $sh.Name -ne "Admin$"){
        Remove-SmbShare -Name $sh.Name -force
        #write-Host($sh.Name)
    }
}

