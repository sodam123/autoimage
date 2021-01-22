$basePath = "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\SCHANNEL"
$keyPath1 = $basePath + "\\Ciphers"
$keyPath2 = $basePath + "\\Protocols" 
$compKeys1 = Get-ChildItem -Name $keyPath1
$compKeys2 = Get-ChildItem -Name $keyPath2
$compKeys1
$compKeys2

$ciphers = @("RC4 128/128", "RC4 40/128", "RC4 56/128", "Triple DES 168")
$protocols = @("SSL 2.0", "SSL 3.0", "TLS 1.0", "TLS 1.1")

############Ciphers#############
#$flag_ci = 0
Foreach($ci in $ciphers){
    #$flag_ci = 0
    Foreach($k1 in $compKeys1){
        #$keypath1 + "\" + $k1
        if($ci -eq $k1){##레지스트리가 있는 경우
           #$flag_ci = 1
            $cpath = $keyPath1 + "\\" + $ci
            Set-itemproperty -path $cpath -Name Enabled -value 0
        }
    }
    <#if($flag_ci -eq 0){##해당 레지스트리가 없는 경우 새로 추가
        $ci -match "/"
        New-Item -path $keyPath1 -Name $ci
        $spath = $keyPath1 + "\\" + $ci
        Set-itemproperty -path $spath -Name Enabled -value 0
    }#>
}


###########Protocols############
#$flag_p = 0
Foreach($p in $protocols){
    #$flag_p = 0
    Foreach($k2 in $compKeys2){
        if($p -eq $k2){
            #$flag_p = 1
            $ppath = $keyPath2 + "\\" + $p
            Set-itemproperty -path $ppath -Name Enabled -value 0
        }
    }
    #if($flag_p -eq 0){} ##새로 추가
}