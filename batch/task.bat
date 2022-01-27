@echo off
rem create windows task: 
rem schtasks /create /tn test2 /tr "cmd /k \"C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\git\scripts\batch\task.bat\"" /sc daily /st 09:59
echo begin > "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\log\task.log"
rem disable global protect:
rem sc stop PanGPS
timeout /t 86400
python -u "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\git\dev_env\sync.py" -d 321ewqdsa.000webhostapp.com -o 1 -m downdata -k <key> -p whatgift  >> "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\log\task.log"
rem enabel global protect:
rem sc start PanGPS
python -u "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\git\scripts\python\daily_downdata.py" -p "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\git\dev_env" >> "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\log\task.log"
echo end  >> "C:\Users\eharvin\OneDrive - Ericsson AB\000Vince\programming\log\task.log"

