#icacls "C:\Users\Administrator\Desktop\test.txt"

#$filename = Get-ChildItem "C:\Users\Administrator\Desktop\test.txt" -force -Recurse

$filepath = "C:\Users\Administrator\Desktop\test.txt"
#$s = Get-ChildItem "C:\Users\Administrator\Desktop\test.txt"

#$temp = icacls "C:\Windows\System32\config\SAM"

#$filepath = "C:\Windows\System32\config\SAM"
#$filename = Get-ChildItem $filepath -Recurse -force #| Select Name,Directory,@{Name="Owner";Expression={(Get-ACL $_.Fullname).Owner}}
#FOREACH-Object {Get-Acl $_.Fullname} |Select-Object pshchildname, path, user, group, @{N='Owner';E={$_.GetAccessControl().Owner}}
#Get-Acl $filepath | Format-List


#Foreach($usr in $filename) {
    #$f = Get-Acl $usr.Fullname
    #$a = @((Get-Acl $filepath).Access | Select-Object -ExpandProperty IdentityReference)
    #$b = $a.Value.Split("\")
    $a = @((Get-Acl $filepath)).Access
    Foreach($ele in $a){
        $b,$c = $ele.IdentityReference.Value.split("\")
        write($c)
        if(($c -ne "SYSTEM") -and ($c -ne "Administrator")){
            #icacls $filename /grant "$c :(OI)(CI)(F)"
            icacls $filepath /inheritance:d
            icacls $filepath /remove "$c"
            icacls $filepath /reset
            #icacls $filepath /inheritance:e
        }
    }
    #$CurUsr = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    #$usersid = New-Object System.Security.Principal.Ntaccount ($CurUsr)
    #write-host($usersid)
<#Foreach($ele in $a){

    $author, $usrname = ($ele.value.ToString()).Split("\")
    #$usrname = $aa.split("\")
    if(($usrname -ne "SYSTEM") -and ($usrname -ne "Administrator")){
        write-host($usrname)
        #$usrid = Get-Variable $usrname[1]
        icacls $filepath /grant $usrname

    }

    write("--------------")
}#>
    
#}
