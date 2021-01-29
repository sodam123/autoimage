import os
import os.path
import sys
import platform
import subprocess
import wget
import shutil
import time
import winreg as reg
import math
from tqdm import tqdm
from subprocess import Popen
from winScriptList import win_2012_std_scripts, win_2012_r2_std_scripts, win_2016_std_scripts, win_2019_std_scripts
from winScriptList import win_2012_std_scripts_mssql, win_2012_r2_std_scripts_mssql, win_2016_std_scripts_mssql, win_2019_std_scripts_mssql


#os_name = os_fullname = ""
#mssql_name = []
#mssql_version = mssql_edition = "null"

original_url = "http://mirror.g.ucloudbiz.com"

base_path = "http://14.63.164.24/epc_repo/template_utils/Windows"
win_path = "http://14.63.164.24/epc_repo/window-init-script/init-script-executor"
initscr_path = "C:\\Windows\\Setup"

def bar_custom(current, total, width=80):
    width=30
    avail_dots = width-2
    shaded_dots = int(math.floor(float(current) / total * avail_dots))
    percent_bar = '[' + '■'*shaded_dots + ' '*(avail_dots-shaded_dots) + ']'
    progress = "%d%% %s [%d / %d]" % (current / total * 100, percent_bar, current, total)
    return progress

def run(cmd):
    completed = subprocess.run(["powershell","-ExecutionPolicy","Bypass",cmd], shell = True)#stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return completed

######취약점 조치1(완료) - ncpa.cpl실행 > NetBIOS over TCP/IP 사용안함으로 설정(기본값: 0 사용함: 1 사용안함 2)########

#한줄 명령어 코드#

"""
netBios_unable = '(Get-WmiObject Win32_NetworkAdapterConfiguration -Filter IpEnabled="true").SetTcpipNetbios(2)'
subprocess.call(["powershell",netBios_unable],shell = True)
"""


def netBios_TCPIP_Off():

    tmp = os.getcwd()
    filepath = tmp + "\\netBios.ps1"
    netBios_info = run(filepath)
    
    
    if netBios_info.returncode != 0:
        print("An error occured: %s", netBios_info.stderr)
    else:
        #print("취약점 조치1 command executed successfully!")
        print("> 'NetBIOS over TCP/IP' -> '사용안함' 으로 설정되었습니다.")
        
    time.sleep(1.5)
    #print("=======================================================================")
    


######취약점 조치2(완료) - C:\Windows\system32\config\SAM파일 우클릭 > 속성 > 보안탭에서 Administrator, System 그룹외 다른 사용자 삭제######

def SAM_rmUser():

    tmp = os.getcwd()
    filepath = tmp + "\\rmUser.ps1"
    user_info = run(filepath)
    
    
    if user_info.returncode != 0:
        print("An error occured: %s", user_info.stderr)
    else:
        #print("취약점 조치2 command executed successfully!")
        print("> SAM파일 내 불필요한 사용자 그룹이 모두 삭제되었습니다.")
    
    time.sleep(1.5)
    #print("-------------------------")





######취약점 조치3(완료) - 로컬보안 정책 > 보안 옵션 > SAM계정 옵션 2개 모두 사용으로 설정######

def SAM_accPolicy_On():

    tmp = os.getcwd()
    filepath = tmp + "\\samOpt.ps1"
    sam_info = run(filepath)
    
    
    if sam_info.returncode != 0:
        print("An error occured: %s", sam_info.stderr)
    else:
        #print("취약점 조치3 command executed successfully!")
        print("> 'SAM 계정과 공유의 익명 열거 허용안함' -> '사용' 으로 설정되었습니다.")
        time.sleep(1.5)
        print("> 'SAM 계정의 익명 열거 허용안함' -> '사용' 으로 설정되었습니다.")
    
    time.sleep(1.5)
    #print("-------------------------")



######취약점 조치4(완료) - 컴퓨터 관리 > 공유 폴더 > 공유에서 불필요한 기본 공유 '공유 중지' 설정 // 레지스트리 값 변경######

def stopShare():

    ##########공유 폴더 중지하는 부분############

    tmp = os.getcwd()
    filepath = tmp + "\\shFile.ps1"
    shFile_info = run(filepath)
    
    
    if shFile_info.returncode != 0:
        print("An error occured: %s", shFile_info.stderr)
    else:
        #print("취약점 조치4-1 command executed successfully!")
        print("> 공유 폴더 내 불필요한 공유 설정이 모두 중지되었습니다.")

    time.sleep(1.5)
    #print("-------------------------")

    assReg = "REG ADD HKLM\\System\\CurrentControlSet\\Services\\LanmanServer\\parameters /v AutoShareServer /t REG_DWORD /d 0 /f"
    #reg_info = subprocess.getstatusoutput(assReg)
    reg_info = subprocess.run(assReg, stdout = subprocess.PIPE)
    
    if reg_info.returncode != 0:
        print("An error occured: %s", reg_info.stderr)
    else:
        #print("취약점 조치4-2 command executed successfully!")
        print("> AutoShareServer 레지스트리 값이 0으로 설정되었습니다.")

    time.sleep(1.5)
    #print("-------------------------")




######취약점 조치5(완료) - 445포트 오픈 후 바로 차단 > 445포트 없음 확인######

def stop445port():

    tmp = os.getcwd()
    filepath = tmp + "\\banport.ps1"
    banport_info = run(filepath)
    
    
    if banport_info.returncode != 0:
        print("An error occured: %s", banport_info.stderr)
    else:
        #print("취약점 조치5 command executed successfully!")
        print("> 445포트 차단 조치가 완료되었습니다.(재부팅시 포트 차단 완료)")

    time.sleep(1.5)
    #print("-------------------------")



######취약점 조치6(완료) - 레지스트리 편집 > 프로토콜 레지스트리에 Enabled 추가######

def addEnabledReg() :

    tmp = os.getcwd()
    filepath = tmp + "\\addReg.ps1"
    addReg_info = run(filepath)
    
    
    if addReg_info.returncode != 0:
        print("An error occured: %s", addReg_info.stderr)
    else:
        #print("취약점 조치6 command executed successfully!")
        print("> 프로토콜 레지스트리와 취약 알고리즘 레지스트리가 모두 비활성되었습니다.")
    
    time.sleep(1.5)
    #print("-------------------------")

################################################################################################################################################
################################################################################################################################################


def make_dir(name) :

    if not os.path.isdir(name):
        os.makedirs(name)
        #print("make")

    #else:
        #print("already existed")

def file_exist_check(front,end):

    if(os.path.isfile(front + "/" + end)):
        os.remove(front + "/" + end)
        #print("REMOVE " + end)
        
def get_winos_fullname():
    
    key = reg.HKEY_LOCAL_MACHINE
    key_value = "Software\Microsoft\Windows NT\CurrentVersion"

    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)

    try:
        value, type = reg.QueryValueEx(open,"ProductName")
        #print(value,"Type:",type)

    except FileNotFoundError:
        print("AutoConfigURL not found")
    
    reg.CloseKey(open)

    return value

def check_mssql() :

    file_exist_check("C:","mssql_test.txt")

    tmp = os.getcwd()
    filepath = tmp + "\\checkSQL.ps1"
    checkSQL_info = run(filepath)

    with open("C:\mssql_test.txt",'r') as fp:
        mssql_name = fp.read().splitlines()
    
    return mssql_name
    #print(mssql_name)

def Copy_UerdataExcutor() :

    uni_pathb = "/UserDataExecutor/WindowsUserdataExecutor_powershell.bat"
    uni_pathp = "/UserDataExecutor/uerdataexecutor.ps1"

    dest_path = "C:/Windows/Setup/Scripts"

    file_name1 = "WindowsUserdataExecutor_powershell.bat"
    file_name2 = "uerdataexecutor.ps1"

    file_exist_check(dest_path,file_name1)
    file_exist_check(dest_path,file_name2)

    
    urls_bat = base_path + uni_pathb
    urls_ps = base_path + uni_pathp

    wget.download(urls_bat, dest_path, bar = bar_custom)
    print(" GET " + file_name1)

    time.sleep(1)

    wget.download(urls_ps, dest_path, bar = bar_custom)
    print(" GET " + file_name2)

    
    #copy(dir_file1, dest_path)
    #copy(dir_file2, dest_path)
    # os.remove('C:\\Windows\Setup\Scripts\WindowsUserdataExecutor_powershell.bat')

def Copy_And_Execute_TimeSettingScript() :

    uni_path = "/timeSetting/timeSetting.bat"
    dest_path = 'C:/Windows'
    file_name = 'timeSetting.bat'

    file_exist_check(dest_path,file_name)

    wget.download(base_path + uni_path, dest_path, bar = bar_custom)
    print(" GET ",file_name)

    ######timeSetting.bat파일 1회실행######
    
    #time_info = subprocess.call(["powershell","Start-Process -FilePath C:\\Windows\\timeSetting.bat"],shell=True)
    time_info = subprocess.run([r'C:\\Windows\\timeSetting.bat'])
    
    if(time_info.returncode != 0):
        print("RUN TimeSetting.bat ERROR")
    else:
        print("RUN TimeSetting.bat SUCCESS")

######SKIP REARM######



######################
def Copy_SynctimeScript() :

    uni_path = "/timeSetting/time.bat"
    dest_path = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup'
    file_name = 'time.bat'

    file_exist_check(dest_path,file_name)

    wget.download(base_path + uni_path, dest_path, bar = bar_custom)
    print(" GET ",file_name)


def Check_Firewall() :

    fw_info = subprocess.run("netsh advfirewall set allprofiles state off")


def Copy_InitScript() :

    uni_path = "/SetupComplete/SetupComplete.cmd"
    dest_path = 'C:/Windows/Setup/scripts'
    file_name = 'SetupComplete.cmd'
    
    file_exist_check(dest_path,file_name)

    wget.download(base_path + uni_path, dest_path, bar = bar_custom)
    print(" GET ",file_name)

def Copy_WinInitScript(os_fullname):


    if os_fullname == "Windows Server 2012 Standard" :
        #print(os_fullname)

        uni_path = "/window2012std_init_script.bat"
        dest_path = 'C:/Windows/Setup/Scripts'
        file_name = 'window2012std_init_script.bat'

        file_exist_check(dest_path,file_name)

        wget.download(win_path + uni_path, dest_path, bar = bar_custom)
        print(" GET ",file_name)

    elif os_fullname == "Windows Server 2012 R2 Standard":
        #print(os_fullname)
        
        uni_path = "/window2012r2_init_script.bat"
        dest_path = 'C:/Windows/Setup/Scripts'
        file_name = 'window2012r2_init_script.bat'
        
        wget.download(win_path + uni_path, dest_path, bar = bar_custom)
        print(" GET ",file_name)

    elif os_fullname == "Windows Server 2016 Standard":
        #print(os_fullname)
        
        uni_path = "/window2016std_init_script.bat"
        dest_path = 'C:/Windows/Setup/Scripts'
        file_name = 'window2016std_init_script.bat'
        
        wget.download(win_path + uni_path, dest_path, bar = bar_custom)
        print(" GET ",file_name)
    
    elif os_fullname == "Windows Serer 2019 Standard":
        #print(os_fullname)
        
        uni_path = "/window2019std_init_script.bat"
        dest_path = 'C:/Windows/Setup/Scripts'
        file_name = 'window2019std_init_script.bat'
        
        wget.download(win_path + uni_path, dest_path, bar = bar_custom)
        print(" GET ",file_name)


def Register_Script(os_fullname):

    scr_path = "C:/Windows/System32/GroupPolicy/Machine/Scripts"

    if os_fullname == "Windows Server 2012 Standard" :

        file_exist_check(scr_path,"scripts.ini")
        fo = open(scr_path + "/" + "scripts.ini","w")
        fo.writelines(win_2012_std_scripts)
        fo = os.popen('attrib +h ' + scr_path + "/" + "scripts.ini")

        fo.close()

    elif os_fullname == "Windows Server 2012 R2 Standard":
        
        file_exist_check(scr_path,"scripts.ini")
        fo = open(scr_path + "/" + "scripts.ini","w")
        fo.writelines(win_2012_r2_std_scripts)
        fo = os.popen('attrib +h ' + scr_path + "/" + "scripts.ini")

        fo.close()
    
    elif os_fullname == "Windows Server 2016 Standard":
        
        file_exist_check(scr_path,"scripts.ini")
        fo = open(scr_path + "/" + "scripts.ini","w")
        fo.writelines(win_2016_std_scripts)
        fo = os.popen('attrib +h ' + scr_path + "/" + "scripts.ini")

        fo.close()

    elif os_fullname == "Windows Serer 2019 Standard":
        
        file_exist_check(scr_path,"scripts.ini")
        fo = open(scr_path + "/" + "scripts.ini","w")
        fo.writelines(win_2019_std_scripts)
        fo = os.popen('attrib +h ' + scr_path + "/" + "scripts.ini")

        fo.close()


def Register_Script_Mssql(os_fullname):

    scr_path = "C:/Windows/System32/GroupPolicy/Machine/Scripts"

    if os_fullname == "Windows Server 2012 Standard" :
       
        file_exist_check(scr_path,"scripts.ini")
        fo = open(scr_path + "/" + "scripts.ini","w")
        fo.writelines(win_2012_std_scripts_mssql)
        fo = os.popen('attrib +h ' + scr_path + "/" + "scripts.ini")

        for e in tqdm(range(8)) :

            if e%2 == 1:  
                print("*" + win_2012_r2_std_scripts_mssql[e] + "- 등록 완료")
                time.sleep(1)
        """       
        time.sleep(1)
        print("*window2012std_init_script.bat - 등록 완료")
        time.sleep(1)
        print("*ktconf.bat - 등록 완료")
        time.sleep(1)
        print("*WindowUserdataExecutor_powershell.bat - 등록 완료")
        time.sleep(1)
        """

        fo.close()

    elif os_fullname == "Windows Server 2012 R2 Standard":
        
        file_exist_check(scr_path,"scripts.ini")
        fo = open(scr_path + "/" + "scripts.ini","w")
        fo.writelines(win_2012_r2_std_scripts_mssql)
        fo = os.popen('attrib +h ' + scr_path + "/" + "scripts.ini")

        fo.close()

    elif os_fullname == "Windows Server 2016 Standard":
       
        file_exist_check(scr_path,"scripts.ini")
        fo = open(scr_path + "/" + "scripts.ini","w")
        fo.writelines(win_2016_std_scripts_mssql)
        fo = os.popen('attrib +h ' + scr_path + "/" + "scripts.ini")

        fo.close()
    
    elif os_fullname == "Windows Serer 2019 Standard":
        
        file_exist_check(scr_path,"scripts.ini")
        fo = open(scr_path + "/" + "scripts.ini","w")
        fo.writelines(win_2019_std_scripts_mssql)
        fo = os.popen('attrib +h ' + scr_path + "/" + "scripts.ini")

        fo.close()

def download_mssql_Allneed(version, edition):

    mssql_path = base_path + "/Mssql"
    dest_path1 = "C:/Windows/mssql"
    dest_path2 = "C:/Windows/System32/GroupPolicy/Machine/Scripts/Startup"

    file_inScript = ["autoinstall.bat", "head.bat", "main.bat", "Readme.txt"]
    file_inKT = ["Microsoft.VC90.CRT.manifest", "msvcm90.dll", "msvcr90.dll", "msvcp90.dll", "UcloudService.exe", "Ucloud.dll", "mssqlConfig.log"]

    file_name1 = "autoinstall.bat"
    file_name2 = "ktconf.bat"

    
    ######자동설치 스크립트 복사######
    make_dir(dest_path1 + '/script')
    for scf in file_inScript:
        
        #print(scf)
        #print(mssql_path + "/" + "mssql" + version + edition + "/script" + "/" + scf)
        wget.download(mssql_path + "/" + "mssql" + version + edition + "/script" + "/" + scf , dest_path1 + "/script", bar = bar_custom)
        print(" GET " + scf)

    make_dir(dest_path1 + '/script/kt')    
    for ktf in file_inKT:

        wget.download(mssql_path + "/" + "mssql" + version + edition + "/script/kt" + "/" + ktf , dest_path1 + "/script/kt", bar = bar_custom)
        print(" GET " + ktf)

    print("GET script Directory")

    time.sleep(1)

    file_exist_check(dest_path1,file_name1)
    wget.download(mssql_path + "/" + "mssql" + version + edition + "/script" + "/" + file_name1, dest_path1, bar = bar_custom)
    print(" GET ",file_name1)

    time.sleep(1)

    ######자동설치 script 실행 파일 등록######
    file_exist_check(dest_path2,file_name2)
    wget.download(mssql_path + "/" + "mssql" + version + edition + "/" + file_name2, dest_path2, bar = bar_custom)
    print(" GET ",file_name2)


def Copy_And_Register_AutoExecScript(mssql_version, mssql_edition) :
    
    if mssql_version == "SQL Server 2012" :
        
        if mssql_edition == "Standard Edition" :
            
            download_mssql_Allneed("2012","std")
            
        elif mssql_edition == "Enterprise Edition" :

            download_mssql_Allneed("2012","ent")
    """
    elif mssql_version == "SQL Server 2014" :
        
        if mssql_edition == "Standard Edition" :
            
            download_mssql_Allneed("2014","std")
            
        elif mssql_edition == "Enterprise Edition" :

            download_mssql_Allneed("2014","ent")

    elif mssql_version == "SQL Server 2016" :
        
        if mssql_edition == "Standard Edition" :
            
            download_mssql_Allneed("2016","std")
            
        elif mssql_edition == "Enterprise Edition" :

            download_mssql_Allneed("2016","ent")

    elif mssql_version == "SQL Server 2019" :
        
        if mssql_edition == "Standard Edition" :
            
            download_mssql_Allneed("2019","std")
            
        elif mssql_edition == "Enterprise Edition" :

            download_mssql_Allneed("2019","ent")
    """

def Stop_Cloud_Service() :
    
    #commandstr = "Set-Service -Name 'Cloud.com Instance Manager' -Status stopped -Force -StartupType Manual"
    commandstr1 = "set-service -Name 'Cloud.com Instance Manager' -StartupType Manual"
    subprocess.call(["powershell",commandstr1],shell = True)
    
    commandstr2 = "stop-service -Name 'Cloud.com Instance Manager'"
    subprocess.call(["powershell",commandstr2],shell = True)

def Copy_Mssql_Install_Check_File() :

    mssql_path = base_path + "/Mssql"
    dest_path3 = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup"
    file_name3 = "mssql_install_check.vbs"

    ######Mssql install check 파일 복사######
    file_exist_check(dest_path3,file_name3)
    wget.download(mssql_path + "/" + file_name3, dest_path3, bar = bar_custom)
    print(" GET ",file_name3)

def Sysprep(os_fullname) :


    if os_fullname == "Windows Server 2012 Standard" :

        uni_path = "/Sysprep/2012/2012STD/sysprep2012std/unattend.xml"
        dest_path = 'C:/Windows/System32/Sysprep'
        file_name = 'unattend.xml'

        file_exist_check(dest_path,file_name)

        wget.download(base_path + uni_path, dest_path, bar = bar_custom)
        print(" GET ",file_name)
    
    elif os_fullname == "Windows Server 2012 R2 Standard" :

        uni_path = "/Sysprep/2012/2012R2/sysprep2012r2/unattend-kor.xml"
        dest_path = 'C:/Windows/System32/sysprep'
        file_name = 'unattend.xml'

        file_exist_check(dest_path,file_name)

        wget.download(base_path + uni_path, dest_path, bar = bar_custom)
        os.rename(dest_path + "/" + "unattend-kor.xml", dest_path + "/" + file_name)
        print(" GET ",file_name)
    
    elif os_fullname == "Windows Server 2016 Standard" :

        uni_path = "/Sysprep/2016/2016STD/sysprep2016std/unattend.xml"
        dest_path = 'C:/Windows/System32/sysprep'
        file_name = 'unattend.xml'

        file_exist_check(dest_path,file_name)

        wget.download(base_path + uni_path, dest_path, bar = bar_custom)
        print(" GET ",file_name)

    elif os_fullname == "Windows Serer 2019 Standard":

        uni_path = "/Sysprep/2019/unattend.xml"
        dest_path = 'C:/Windows/System32/sysprep'
        file_name = 'unattend.xml'

        file_exist_check(dest_path,file_name)

        wget.download(base_path + uni_path, dest_path, bar = bar_custom)
        print(" GET ",file_name)

    tmp = os.getcwd()
    filepath = tmp + "\\sysprepEx.ps1"
    sysprepEx_info = run(filepath)

    """
    time.sleep(2)
    commandstr = "Start-Process -FilePath C:\Windows\System32\Sysprep\Sysprep.exe -ArgumentList /oobe /generalize /quit /unattend:unattend.xml"
    commandstr = "start-process sysprep /oobe /generalize /quit /unattend:unattend.xml"
    subprocess.call(["powershell",commandstr],shell = True)
    """
def ubuntu_setting() :

    subprocess.call('chmod 400 /etc/shadow')
    subprocess.call('chown root /etc/shadow')

    subprocess.call('chmod -s /usr/bin/newgrp')
    subprocess.call('chmod -s /sbin/unix_chkpwd')
    subprocess.call('chmod -s /usr/bin/at')


    base_path = "http://14.63.164.24/epc_repo"
    dest_path = '/etc/init.d'
    file_name1 = 'epc-init-script.sh'
    file_name2 = 'userdataExecutor.sh'


    file_exist_check(dest_path,file_name1)

    wget.download(base_path + "/epc-init-script" + "/" + file_name1 + ".bak2" , dest_path, bar = bar_custom)
    os.rename(dest_path + "/epc-init-script.sh.bak2", dest_path + "/" + file_name1)
    print(" GET ", file_name1)

    time.sleep(1)

    file_exist_check(dest_path,file_name2)
    wget.download(base_path + "/userdataExecutor" + "/" + file_name2 , dest_path, bar = bar_custom)
    print(" GET ", file_name2)

    subprocess.call('chmod 755 /etc/init.d/' + file_name1)
    subprocess.call('chmod 755 /etc/init.d/' + file_name2)

    #####rc.local에서 실행후 clean up작업 해야됨#####

def centos_setting() :

    subprocess.call('chmod 755 /usr/bin/newgrp')
    subprocess.call('chmod 755 /sbin/unix_chkpwd')

    base_path = "http://14.63.164.24/epc_repo"
    dest_path = '/etc/init.d'
    file_name1 = 'epc-init-script-v2.sh'
    file_name2 = 'sethostname.sh'
    file_name3 = 'userdataExecutor.sh'


    file_exist_check(dest_path,file_name1)
    wget.download(base_path + "/epc-init-script" + "/" + file_name1 , dest_path, bar = bar_custom)
    print(" GET ", file_name1)

    time.sleep(1)

    file_exist_check(dest_path,file_name2)
    wget.download(base_path + "/sethostname" + "/" + file_name2 , dest_path, bar = bar_custom)
    print(" GET ", file_name2)

    time.sleep(1)

    file_exist_check(dest_path,file_name3)
    wget.download(base_path + "/userdataExecutor" + "/" + file_name3 , dest_path, bar = bar_custom)
    print(" GET ", file_name3)

    subprocess.call('chmod 755 /etc/init.d/epc-init-script-v2.sh')
    subprocess.call('chmod 755 /etc/init.d/sethostname.sh')
    subprocess.call('chmod 755 /etc/init.d/userdataExecutor')

     #####rc.local에서 실행후 clean up작업 해야됨#####

if __name__ == "__main__":

    os_name = platform.system()

    if os_name == "Windows" :

        os_fullname = get_winos_fullname()
        mssql_name = check_mssql()
        
        mssql_version = mssql_name[0]
        mssql_edition = mssql_name[1]

        print("============================= 취약점 조치 시작 =============================")
        
        
        netBios_TCPIP_Off()
        SAM_rmUser()
        SAM_accPolicy_On()
        stopShare()
        stop445port()
        addEnabledReg()
        

        print("============================= 취약점 조치 완료 =============================")
        make_dir(initscr_path + '\Scripts')

        if mssql_version == "null" : ## **NOT MSSQL** ##
        
            print("******Window******")

            print("WINDOW OS VERSION :",os_fullname)
            #Copy_UerdataExcutor()
            #Copy_And_Execute_TimeSettingScript()
            #Copy_SynctimeScript
            #Check_Firewall()
            #Copy_InitScript()
            #Copy_WinInitScript(os_fullname)
            #Register_Script(os_fullname)
            #Sysprep(os_fullname)

        else : ## **MSSQL** ##
            
            print("******Window + Mssql******")

            print("WINDOW OS VERSION :",os_fullname)
            print("MSSQL VERSION :",mssql_version)
            print("MSSQL EDITION :",mssql_edition)

            make_dir('C:/Windows/mssql')
            

            print("Loading...")
            time.sleep(3)
            Copy_And_Register_AutoExecScript(mssql_version, mssql_edition)
            print("> 자동 설치 Script 실행파일이 모두 정상적으로 등록되었습니다.")


            print("Loading...")
            time.sleep(1.5)
            Copy_UerdataExcutor()
            print("> UserdataExecutor스크립트 파일이 모두 정상적으로 등록되었습니다.")

            print("Loading...")
            time.sleep(1.5)
            Copy_SynctimeScript()
            print("> Time 동기화 스크립트 파일이 정상적으로 등록되었습니다.")

            print("Loading...")
            time.sleep(1.5)
            Copy_And_Execute_TimeSettingScript()
            print("> TimeSetting 스크립트 파일이 정상적으로 등록되었습니다.")

            print("Loading...")
            time.sleep(1.5)
            Check_Firewall()
            print("> 윈도우 방화벽 설정이 모두 OFF로 설정되었습니다.")

            print("Loading...")
            time.sleep(1.5)
            Copy_InitScript()
            print("> Init 스크립트 파일이 정상적으로 등록되었습니다.")

            print("Loading...")
            time.sleep(1.5)
            Copy_WinInitScript(os_fullname)
            print("> WindowInitScript파일이 정상적으로 등록되었습니다.")

            print("Loading...")
            time.sleep(1.5)
            Register_Script_Mssql(os_fullname)
            print("> 4개의 스크립트 파일이 시작 프로그램 스크립트 파일로 등록되었습니다.")

            print("Loading...")
            time.sleep(1.5)
            Stop_Cloud_Service()
            print("> Cloud.com 서비스가 중지되었습니다.")

            print("Loading...")
            time.sleep(1.5)
            Copy_Mssql_Install_Check_File()
            print("Mssql install check 파일이 정상적으로 등록되었습니다.")

            print("Loading...")
            time.sleep(1.5)
            #Sysprep(os_fullname)


    """
    elif os_name == "Ubuntu" : ##우분투 Linux##

        ubuntu_setting()

    elif os_name == "CentOS" :

        centos_setting()

    """
