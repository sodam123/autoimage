import os
import os.path
import sys
import platform
import subprocess
import wget
import shutil
import time
import winreg as reg


os_name = platform.system()
mssql_name = platform.system() ##수정필요

original_url = "http://mirror.g.ucloudbiz.com"

base_path = "http://14.63.164.24/epc_repo/template_utils/Windows"
win_path = "http://14.63.164.24/epc_repo/window-init-script/init-script-executor"
initscr_path = "C:\\Windows\\Setup"

win_2012_std_scripts = ['[Startup]\n',
                        '0CmdLine=C:\Windows\Setup\Scripts\SetupComplete.cmd\n',
                        '0Parameters=\n',
                        '1CmdLine=C:\Windows\Setup\Scripts\window2012std_init_script.bat\n',
                        '1Parameters=\n',
                        '2CmdLine=C:\Windows\Setup\Scripts\WindowsUserdataExecutor_powershell.bat\n',
                        '2Parameters=\n']

def run(cmd):
    completed = subprocess.run(["powershell","-ExecutionPolicy","Bypass",cmd], shell = True)#stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return completed

def make_dir(name) :

    if not os.path.isdir(name):
        os.makedirs(name)
        print("make")

    else:
        print("already existed")

def file_exist_check(front,end):

    if(os.path.isfile(front + "/" + end)):
        os.remove(front + "/" + end)
        print("REMOVE " + end)
        

def userdataExcutor() :

    uni_pathb = "/UserDataExecutor/WindowsUserdataExecutor_powershell.bat"
    uni_pathp = "/UserDataExecutor/uerdataexecutor.ps1"

    dest_path = "C:/Windows/Setup/Scripts"

    file_name1 = "WindowsUserdataExecutor_powershell.bat"
    file_name2 = "uerdataexecutor.ps1"

    file_exist_check(dest_path,file_name1)
    file_exist_check(dest_path,file_name2)

    
    urls_bat = base_path + uni_pathb
    urls_ps = base_path + uni_pathp

    wget.download(urls_bat, dest_path)
    print(" GET " + file_name1)
    time.sleep(1)
    wget.download(urls_ps, dest_path)
    print(" GET " + file_name2)

    
    #copy(dir_file1, dest_path)
    #copy(dir_file2, dest_path)
    # os.remove('C:\\Windows\Setup\Scripts\WindowsUserdataExecutor_powershell.bat')

def timeSetting() :

    uni_path = "/timeSetting/timeSetting.bat"
    dest_path = 'C:/Windows'
    file_name = 'timeSetting.bat'

    file_exist_check(dest_path,file_name)

    wget.download(base_path + uni_path, dest_path)
    print(" GET ",file_name)

    """
    time_info = subprocess.run([r'C:\\Windows\\timeSetting.bat'])
    if(time_info.returncode != 0):
        print("RUN TimeSetting.bat ERROR")
    else:
        print("RUN TimeSetting.bat SUCCESS")
    """

######SKIP REARM######



######################
def synctime() :

    uni_path = "/timeSetting/time.bat"
    dest_path = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup'
    file_name = 'time.bat'

    file_exist_check(dest_path,file_name)

    wget.download(base_path + uni_path, dest_path)
    print(" GET ",file_name)


def check_firewall() :

    fw_info = subprocess.run("netsh advfirewall set allprofiles state off")


def scr_init() :

    uni_path = "/SetupComplete/SetupComplete.cmd"
    dest_path = 'C:/Windows/Setup/scripts'
    file_name = 'SetupComplete.cmd'
    
    file_exist_check(dest_path,file_name)

    #wget.download(base_path + "/Mssql/mssql2012std/script", 'C:/Windows/Setup')
    #subprocess.run('wget -r --no-parent --reject "index.html*" http://14.63.164.24:22/epc_repo/template_utils/Windows/Mssql/mssql2012std/script/)
    wget.download(base_path + uni_path, dest_path)
    print(" GET ",file_name)
    #make_dir(first_path)

def get_os_name():

    """
    tmp = os.getcwd()
    filepath = tmp + "\\osName.ps1"
    osName_info = run(filepath)

    return osName_info

    """
    key = reg.HKEY_LOCAL_MACHINE
    key_value = "Software\Microsoft\Windows NT\CurrentVersion"

    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)

    try:
        value, type = reg.QueryValueEx(open,"ProductName")
        print(value,"Type:",type)

    except FileNotFoundError:
        print("AutoConfigURL not found")
    
    reg.CloseKey(open)

    return value

def scr_reg(os_name):

    if os_name == "Windows":

        #os_fullname = platform.platform()[0:12]
        os_fullname = get_os_name()
        scr_path = "C:/Windows/System32/GroupPolicy/Machine/Scripts"
        print("**" + os_fullname)


        if os_fullname == "Windows Server 2012 Standard" :
            #print(os_fullname)

            uni_path = "/window2012std_init_script.bat"
            dest_path = 'C:/Windows/Setup/Scripts'
            file_name = 'window2012std_init_script.bat'

            """
            if(os.path.isfile(dest_path + "/" + file_name)):
                os.remove(dest_path + "/" + file_name)
                print("REMOVE " + file_name)
            """

            file_exist_check(dest_path,file_name)

            wget.download(win_path + uni_path, dest_path)
            print(" GET ",file_name)

            file_exist_check(scr_path,"scripts.ini")
            fo = open(scr_path + "/" + "scripts.ini","w")
            fo.writelines(win_2012_std_scripts)
            fo = os.popen('attrib +h ' + scr_path + "/" + "scripts.ini")

            fo.close()

        elif os_fullname == "Windows Server 2012 R2 Standard":
            print(os_fullname)
            uni_path = "/window2012r2_init_script.bat"
            dest_path = 'C:/Windows/Setup/Scripts'
            file_name = 'window2012r2_init_script.bat'
            wget.download(win_path + uni_path, dest_path)
            print(" GET ",file_name)

        elif os_fullname == "Windows Server 2016 Standard":
            print(os_fullname)
            uni_path = "/window2016std_init_script.bat"
            dest_path = 'C:/Windows/Setup/Scripts'
            file_name = 'window2016std_init_script.bat'
            wget.download(win_path + uni_path, dest_path)
            print(" GET ",file_name)
        
        elif os_fullname == "Windows Serer 2019 Standard":
            print(os_fullname)
            uni_path = "/window2019std_init_script.bat"
            dest_path = 'C:/Windows/Setup/Scripts'
            file_name = 'window2019std_init_script.bat'
            wget.download(win_path + uni_path, dest_path)
            print(" GET ",file_name)
        

    #elif os_name == "Ubuntu":

    #elif os_name == "CentOS":


def reg_initScript():

    tmp = os.getcwd()
    filepath = tmp + "\\regScript.ps1"
    regScript_info = run(filepath)
    #regScript_info = subprocess.run(["cmd","-ExecutionPolicy","Bypass",filepath], shell = True)#stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

def sysprep() :

    if os_name == "Windows" :

        os_fullname = get_os_name()

        if os_fullname == "Windows Server 2012 Standard" :

            uni_path = "/Sysprep/2012/2012STD/sysprep2012std/unattend.xml"
            dest_path = 'C:/Windows/System32/sysprep'
            file_name = 'unattend.xml'

            file_exist_check(dest_path,file_name)

            wget.download(base_path + uni_path, dest_path)
            print(" GET ",file_name)
        
        elif os_fullname == "Windows Server 2012 R2 Standard" :

            uni_path = "/Sysprep/2012/2012R2/sysprep2012r2/unattend-kor.xml"
            dest_path = 'C:/Windows/System32/sysprep'
            file_name = 'unattend.xml'

            file_exist_check(dest_path,file_name)

            wget.download(base_path + uni_path, dest_path)
            os.rename(dest_path + "/" + "unattend-kor.xml", dest_path + "/" + file_name)
            print(" GET ",file_name)
        
        elif os_fullname == "Windows Server 2016 Standard" :

            uni_path = "/Sysprep/2016/2016STD/sysprep2016std/unattend.xml"
            dest_path = 'C:/Windows/System32/sysprep'
            file_name = 'unattend.xml'

            file_exist_check(dest_path,file_name)

            wget.download(base_path + uni_path, dest_path)
            print(" GET ",file_name)

        elif os_fullname == "Windows Serer 2019 Standard":

            uni_path = "/Sysprep/2019/unattend.xml"
            dest_path = 'C:/Windows/System32/sysprep'
            file_name = 'unattend.xml'

            file_exist_check(dest_path,file_name)

            wget.download(base_path + uni_path, dest_path)
            print(" GET ",file_name)


def download_mssql_Allneed(version, edition):

    mssql_path = base_path + "/Mssql"
    dest_path1 = "C:/windows/mssql"
    dest_path2 = "C:/Windows/System32/GroupPolicy/Machine/Scripts/Startup"
    dest_path3 = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup"

    file_inScript = ["autointsall.bat", "head.bat", "main.bat", "Readme.txt"]
    file_inKT = ["Microsoft.VC90.CRT.manifest", "msvcm90.dll", "msvcr90.dll", "msvcp90.dll", "UcloudService.exe", "Ucloud.dll", "mssqlConfig.log"]

    file_name1 = "autoinstall.bat"
    file_name2 = "ktconf.bat"
    file_name3 = "mssql_install_check.vbs"

    ######자동설치 스크립트 복사######
    make_dir(dest_path1 + '/script')
    for scf in file_inScript:

        wget.download(mssql_path + "/" + "mssql" + version + edition + "/script" + scf , dest_path1 + '/script')
        print(" GET " + scf)

    make_dir(dest_path1 + '/script/kt')    
    for ktf in file_inKT:

        wget.download(mssql_path + "/" + "mssql" + version + edition + "/script/kt" + scf , dest_path1 + '/script/kt')
        print(" GET " + ktf)

    print("GET script Directory")

    time.sleep(1)

    file_exist_check(dest_path1,file_name1)
    wget.download(mssql_path + "/" + "mssql" + version + edition + "/script" + file_name1, dest_path1)
    print(" GET ",file_name1)

    time.sleep(1)

    ######자동설치 script 실행 파일 등록######
    file_exist_check(dest_path2,file_name2)
    wget.download(mssql_path + "/" + "mssql" + version + edition + "/" + file_name2, dest_path2)
    print(" GET ",file_name2)

    time.sleep(1)

    ######Mssql install check 파일 복사######
    file_exist_check(dest_path3,file_name3)
    wget.download(mssql_path + "/" + file_name3, dest_path3)
    print(" GET ",file_name3)


def scr_mssql(mssql_name) :
    
    if "2012" in mssql_name :
        
        if "Standard" in mssql_name :
            
            download_mssql_Allneed("2012","std")
            
        elif "Enterprise" in mssql_name :

            download_mssql_Allneed("2012","ent")
    """
    elif "2014" in mssql_name :
    
        if "Standard" in mssql_name :

        elif "Enterprise" in mssql_name :

    elif "2016" in mssql_name :

        if "Standard" in mssql_name :

        elif "Enterprise" in mssql_name :

    elif "2019" in mssql_name :
    
        if "Standard" in mssql_name :

        elif "Enterprise" in mssql_name :
    """

def stopCloud() :
    
    commandstr = "Set-Service -Name 'Cloud.com Instance Manager' -Status stopped -StartupType Manual -Force"
    subprocess.call(["powershell",commandstr],shell = True)

if __name__ == "__main__":



    make_dir(initscr_path + '\Scripts')
 

    #_os = platform.platform()[0:12]
    #print(_os)

    #if "SQL server" :
    
    make_dir('C:/Windows/mssql')
        #scr_mssql(mssql_name)
        #uerdataExcutor()
        #scr_init()
        #scr_reg_mssql(os_name)
    stopCloud()
    #else :
        #uerdataExcutor()
        #timeSetting()
        #skipRearm()
        #synctime()
        #check_firewall()
        #scr_init()
        #scr_reg(os_name)
        #reg_initScript()
        #sysprep()