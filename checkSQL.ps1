
##sql 설치가 되어 있는경우##
if (Test-Path "HKLM:\Software\Microsoft\Microsoft SQL Server\Instance Names\SQL") {
    
    write-host("True")
    #$inst = (get-itemproperty 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server').InstalledInstances
    $var = Get-ItemProperty -path 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\Instance Names\SQL' -Name "SYSPREP"

    $p = $var.sysprep
    $editionname = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\$p\Setup").Edition
    $ver = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\$p\Setup").Version    
    
    switch -wildcard($ver){

        "15*" {$versionname = "SQL Server 2019";}
        "14*" {$versionname = "SQL Server 2017";}
        "13*" {$versionname = "SQL Server 2016";}
        "12*" {$versionname = "SQL Server 2014";}
        "11*" {$versionname = "SQL Server 2012";}
        "10.5*" {$versionname = "SQL Server 2008 R2";}
        "10.4*" {$versionname = "SQL Server 2008";}
        "10.3*" {$versionname = "SQL Server 2008";}
        "10.2*" {$versionname = "SQL Server 2008";}
        "10.1*" {$versionname = "SQL Server 2008";}
        "10.0*" {$versionname = "SQL Server 2008";}
        "9*" {$versionname = "SQL Server 2005";}
        "8*" {$versionname = "SQL Server 2000";}
        default {$versionname = "null";}
    }

    $ver
    $versionname
    $editionname

    $res = $versionname + "`r`n" + $editionname
    Set-Content "C:\mssql_test.txt" $res

}

##sql 설치가 되어 있지 않은 경우
else {

    write-host("False")
    Set-Content "C:\mssql_test.txt" "null`r`nnull"
}
<#
 $osname = (Get-WmiObject Win32_OperatingSystem).Name#.split("|")
 write-host($osname)
 #>

 <#
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
#>