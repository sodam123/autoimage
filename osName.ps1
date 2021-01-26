
<#
 $osname = (Get-WmiObject Win32_OperatingSystem).Name#.split("|")
 write-host($osname)
 #>

 
$flag = "null"

try{
    $inst = (get-itemproperty 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server').InstalledInstances

    catch{
        write-host("something error")
    }

    foreach ($i in $inst)
    {
    $p = (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\Instance Names\SQL').$i
    (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\$p\Setup").Edition
    (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\$p\Setup").Version
    }
}

catch{
    Set-Content "C:\test.txt" $flag
}