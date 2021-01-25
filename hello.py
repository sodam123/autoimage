import os
import subprocess, sys
from subprocess import Popen


def run(cmd):
    completed = subprocess.run(["powershell","-ExecutionPolicy","Bypass",cmd], shell = True)#stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return completed


######취약점 조치1(완료) - ncpa.cpl실행 > NetBIOS over TCP/IP 사용안함으로 설정(기본값: 0 사용함: 1 사용안함 2)########

#한줄 명령어 코드#
"""
netBios_unable = '(Get-WmiObject Win32_NetworkAdapterConfiguration -Filter IpEnabled="true").SetTcpipNetbios(2)'
subprocess.call(["powershell",netBios_unable],shell = True)
"""

"""
if __name__ == '__main__':

    tmp = os.getcwd()
    filepath = tmp + "\\netBios.ps1"
    netBios_info = run(filepath)
    
    
    if netBios_info.returncode != 0:
        print("An error occured: %s", netBios_info.stderr)
    else:
        print("취약점 조치1 command executed successfully!")
    
    print("-------------------------")
    
"""
"""
######취약점 조치2(완료) - C:\Windows\system32\config\SAM파일 우클릭 > 속성 > 보안탭에서 Administrator, System 그룹외 다른 사용자 삭제######

if __name__ == '__main__':

    tmp = os.getcwd()
    filepath = tmp + "\\rmUser.ps1"
    user_info = run(filepath)
    
    
    if user_info.returncode != 0:
        print("An error occured: %s", user_info.stderr)
    else:
        print("취약점 조치2 command executed successfully!")
    
    print("-------------------------")


"""

"""
######취약점 조치3(완료) - 로컬보안 정책 > 보안 옵션 > SAM계정 옵션 모두 사용으로 설정######

if __name__ == '__main__':

    tmp = os.getcwd()
    filepath = tmp + "\\samOpt.ps1"
    sam_info = run(filepath)
    
    
    if sam_info.returncode != 0:
        print("An error occured: %s", sam_info.stderr)
    else:
        print("취약점 조치3 command executed successfully!")
    
    print("-------------------------")
"""


"""
######취약점 조치4(완료) - 컴퓨터 관리 > 공유 폴더 > 공유에서 불필요한 기본 공유 '공유 중지' 설정 // 레지스트리 값 변경######

if __name__ == '__main__':

    ##########공유 폴더 중지하는 부분############

    tmp = os.getcwd()
    filepath = tmp + "\\shFile.ps1"
    shFile_info = run(filepath)
    
    
    if shFile_info.returncode != 0:
        print("An error occured: %s", shFile_info.stderr)
    else:
        print("취약점 조치4-1 command executed successfully!")
    
    print("-------------------------")

    assReg = "REG ADD HKLM\\System\\CurrentControlSet\\Services\\L0anmanServer\\parameters /v AutoShareServer /t REG_DWORD /d 0 /f"
    #reg_info = subprocess.getstatusoutput(assReg)
    reg_info = subprocess.run(assReg, stdout = subprocess.PIPE)
    
    if reg_info.returncode != 0:
        print("An error occured: %s", reg_info.stderr)
    else:
        print("취약점 조치4-2 command executed successfully!")
    
    print("-------------------------")

"""
######취약점 조치5(완료) - 445포트 오픈 후 바로 차단 > 445포트 없음 확인######

if __name__ == '__main__':

    tmp = os.getcwd()
    filepath = tmp + "\\banport.ps1"
    banport_info = run(filepath)
    
    
    if banport_info.returncode != 0:
        print("An error occured: %s", banport_info.stderr)
    else:
        print("취약점 조치5 command executed successfully!")
    
    print("-------------------------")


"""
######취약점 조치6(완료) - 레지스트리 편집 > 프로토콜 레지스트리에 Enabled 추가######

if __name__ == '__main__':

    tmp = os.getcwd()
    filepath = tmp + "\\addReg.ps1"
    addReg_info = run(filepath)
    
    
    if addReg_info.returncode != 0:
        print("An error occured: %s", addReg_info.stderr)
    else:
        print("취약점 조치6 command executed successfully!")
    
    print("-------------------------")
"""