import os
import subprocess, sys
from subprocess import Popen


#os.path.abspath("C:\\WINDOW\\system32")
#os.chdir("\\Users")
#os.chdir("\\WINDOWS\\system32")

######취약점 조치1 - ncpa.cpl실행 > NetBIOS over TCP/IP 사용안함으로 설정(기본값: 0 사용함: 1 사용안함 2)########

#한줄 명령어 코드#
"""
netBios_unable = '(Get-WmiObject Win32_NetworkAdapterConfiguration -Filter IpEnabled="true").SetTcpipNetbios(2)'
subprocess.call(["powershell",netBios_unable],shell = True)
"""

def run(cmd):
    completed = subprocess.run(["powershell","-ExecutionPolicy","Bypass",cmd], shell = True)#stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return completed

if __name__ == '__main__':

    tmp = os.getcwd()
    filepath = tmp + "\\netBios.ps1"
    netBios_info = run(filepath)
    
    
    if netBios_info.returncode != 0:
        print("An error occured: %s", netBios_info.stderr)
    else:
        print("Hello command executed successfully!")
    
    print("-------------------------")
    


######취약점 조치2 - C:\Windows\system32\config\SAM파일 우클릭 > 속성 > 보안탭에서 Administrator, System 그룹외 다른 사용자 삭제######
