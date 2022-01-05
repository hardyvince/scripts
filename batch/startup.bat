@echo off
rem start auto sync, filesync, host trigger/data save
rem add startup.bat - Shortcut to startup apps
rem target of Shortcut: "C:\Program Files\Git\git-cmd.exe" "startup.bat"
rem Start in of Shorcut: "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\git\"
rem startup.bat should placed at any path of Path environment or add full path to the target of Shortcut
rem The All Users Startup Folder is located at the following path: C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp.
rem The Current User Startup Folder is located here: C:\Users\[User Name]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.

start "sync dev_env" python scripts\python\auto_sync_git_diff_to_gdrive.py -p "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\git\dev_env"
start "sync scripts" python scripts\python\auto_sync_git_diff_to_gdrive.py -p "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\git\scripts"
start "sync kisokos" python scripts\python\file_sync_to_gdrive_windows.py

:loop
python dev_env\sync.py -d 321ewqdsa.000webhostapp.com -o 1 -m downdata -k key -p whatgift
timeout /t 86400
goto loop
