import os
import os.path
import sys
import platform
import subprocess
import wget
import shutil
import time
import winreg as reg

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

def check_os(os_name):

    if os_name == "Windows":

        #os_fullname = platform.platform()[0:12]
        os_fullname = get_os_name()
        scr_path = "C:/Windows/System32/GroupPolicy/Machine/Scripts"
        print("**" + os_fullname)
        if os_fullname == "Windows Server 2012 Standard":
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

if __name__ == "__main__":



    make_dir(initscr_path + '\Scripts')

    os_name = platform.system() 

    #_os = platform.platform()[0:12]
    #print(_os)

    #uerdataExcutor()
    #timeSetting()
    #skipRearm()
    #synctime()
    #check_firewall()
    #scr_init()
    check_os(os_name)
    #reg_initScript()