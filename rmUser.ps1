#icacls "C:\Users\Administrator\Desktop\test.txt"

#$filename = Get-ChildItem "C:\Users\Administrator\Desktop\test.txt" -force -Recurse

#$filepath = "C:\Users\Administrator\Desktop\test.txt"
$filepath = "C:\Windows\System32\config\SAM"
#$s = Get-ChildItem "C:\Users\Administrator\Desktop\test.txt"

#$temp = icacls "C:\Windows\System32\config\SAM"
#$filename = Get-ChildItem $filepath -Recurse -force #| Select Name,Directory,@{Name="Owner";Expression={(Get-ACL $_.Fullname).Owner}}
#FOREACH-Object {Get-Acl $_.Fullname} |Select-Object pshchildname, path, user, group, @{N='Owner';E={$_.GetAccessControl().Owner}}
#Get-Acl $filepath | Format-List

#$CurUsr = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
#$usersid = New-Object System.Security.Principal.Ntaccount ($CurUsr)
#write-host($usersid)

<#$acl = Get-ACL 't:\89\src'
$rules = $acl.access | Where-Object { 
    (-not $_.IsInherited) -and 
    $_.IdentityReference -like "DOMAIN\*" 
}
ForEach($rule in $rules) {
    $acl.RemoveAccessRule($rule) | Out-Null
}
Set-ACL -Path 't:\89\src' -AclObject $acl#>

$a = @((Get-Acl $filepath)).Access
Foreach($ele in $a){
    $b,$c = $ele.IdentityReference.Value.split("\")
    write($c)
    if(($c -ne "SYSTEM") -and ($c -ne "Administrator") -and ($c -ne "Administrators")){
        #icacls $filepath /inheritance:d
        icacls $filepath /remove "$c"
        write($c + " REMOVED!")
        icacls $filepath /reset
        #icacls $filepath /inheritance:e
    }
}
   