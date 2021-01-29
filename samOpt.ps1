secedit /export /cfg c:\secpol.cfg
(gc C:\secpol.cfg).replace("RestrictAnonymous=4,0", "RestrictAnonymous=4,1") | Out-File C:\secpol.cfg
(gc C:\secpol.cfg).replace("RestrictAnonymousSAM=4,0", "RestrictAnonymousSAM=4,1") | Out-File C:\secpol.cfg
secedit /configure /db c:\windows\security\local.sdb /cfg c:\secpol.cfg /areas SECURITYPOLICY
rm -force c:\secpol.cfg -confirm:$false