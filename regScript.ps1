# Define output file
$outfile = "c:\temp\sqlversioncheck.csv";
 
# Get all server names from the saved txt file
$adservers = get-adcomputer -filter {operatingsystem -like "*server*"} -properties lastlogondate, operatingsystem |  where {$_.lastlogondate -gt (get-date).adddays(-60)};
 
# Loop through each server 
foreach ($adserver in $adservers) {
 
    $out = $null;
    $server = $adserver.name;
 
    # Check if computer is online
    if (test-connection -computername $server -count 1 -ea 0) {
 
        try {
 
            # Define SQL instance registry keys
            $type = [Microsoft.Win32.RegistryHive]::LocalMachine;
            $regconnection = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey($type, $server);
            $instancekey = "SOFTWARE\Microsoft\Microsoft SQL Server\Instance Names\SQL";
 
            $openinstancekey = $regconnection.opensubkey($instancekey);
 
            # If  registry keys don't exist, try legacy keys
            if ($openinstancekey -eq $null) {
 
                $sqlserverkey = "SOFTWARE\Microsoft\Microsoft SQL Server";
 
                $opensqlkey = $regconnection.opensubkey($sqlserverkey);
                $instances = $opensqlkey.getvalue("InstalledInstances");
 
            # Extract "full" instance names for non-legacy instances.
            } else {
 
               [System.Collections.ArrayList]$instances = @();
 
                foreach ($instance in $openinstancekey.getvaluenames()) {
 
                    $instancename = $openinstancekey.getvalue($instance);
                    [void]$instances.add($instancename);
                }
            }  
 
            if ($instances) {        
 
                # Loop through each instance found
                foreach ($instance in $instances) {
 
                    # Define and open SQL registry keys
                    $instancekey = "SOFTWARE\Microsoft\Microsoft SQL Server\" + $instance; 
                    $openinstancekey = $regconnection.opensubkey($instancekey);
 
                    if ($openinstancekey) {
 
                        # Get instance name
                        $instancename = $openinstancekey.getvalue("")
 
                        # Check for legacy intance name information
                        if ($instancename -eq $null) {
 
                            $instancename = $instance
                        }
 
                        # Define and open SQL setup registry keys
                        $instancesetupkey = "SOFTWARE\Microsoft\Microsoft SQL Server\" + $instance + "\Setup"; 
                        $openinstancesetupkey = $regconnection.opensubkey($instancesetupkey);
 
                        # Get Edition
                        $edition = $openinstancesetupkey.getvalue("Edition")
 
                        # Check for legacy edition information
                        if ($edition -eq $null) {
 
                            $edition = "N/A";
                        }
 
                        # Get Version
                        $version = $openinstancesetupkey.getvalue("Version");
 
                        # Check for legacy version information
                        if ($version -eq $null) {
 
                            $currentversionkey = "SOFTWARE\Microsoft\Microsoft SQL Server\" + $instance + "\MSSQLServer\CurrentVersion"; 
                            $opencurrentversionkey = $regconnection.opensubkey($currentversionkey);
                            $version = $opencurrentversionkey.getvalue("CSDVersion");
 
                        }
 
                        switch -wildcard ($version) {
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
                            default {$versionname = $version;}
                        }
 
                        # Output results 
                        $out =  $server + "^" + $instancename + "^" + $edition + "^" + $versionname; 
                        $out >> $outfile;                   
                    } 
                }
            } else {
 
                $out = $server + "^Could not find/open SQL registry keys";
                $out >> $outfile;
                
            }
        } catch {
 
            $out = $server + "^Could not find/open SQL registry keys";
            $out >> $outfile;
        }
    }
    else {
 
        $out = $server + "^Not online";
        $out >> $outfile;
    }
}
 