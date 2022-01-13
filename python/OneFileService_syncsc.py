#pip install pypiwin32
#python myvenv\Scripts\pywin32_postinstall.py -install
#or add to path the C:\Python\Python310\lib\site-packages\pywin32_system32 where the dll-s live
#register the dll-s and copy to C:\Windows\System32???
import socket

import win32serviceutil

import servicemanager
import win32event
import win32service
import time
from datetime import datetime

import sys

import auto_sync_git_diff_to_gdrive 


def WriteToFile():
    DIR = "C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\log\\file.txt"
    while True:
        time.sleep(1)
        with open(DIR,'a+') as file:
            file.write(str(datetime.now()))
        file.close()


dwCurrentState = {
5: "SERVICE_CONTINUE_PENDING", 
6: "SERVICE_PAUSE_PENDING", 
7: "SERVICE_PAUSED", 
4: "SERVICE_RUNNING", 
2: "SERVICE_START_PENDING", 
3: "SERVICE_STOP_PENDING", 
1: "SERVICE_STOPPED"  }



class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = 'syncsc'
    _svc_display_name_ = 'Sync scripts'
    #_svc_description_ = 'Python Service Description'

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        auto_sync_git_diff_to_gdrive.observer_stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        self.isrunning = True

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        self.isrunning = False

    def main(self):
        auto_sync_git_diff_to_gdrive.main(['auto_sync_git_diff_to_gdrive.py', '-p', 'C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\git\\scripts'])

# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    #SMWinservice.main(SMWinservice)
    if len(sys.argv) != 1 and sys.argv[1] == "status":
        try: 
            serviceStatus = win32serviceutil.QueryServiceStatus('syncsc')        
        except:
            print("Windows service NOT installed")
        else:
            print(serviceStatus)
            print(serviceStatus[1])
            print(dwCurrentState[serviceStatus[1]])
            print("Windows service installed")
    else:
        SMWinservice.parse_command_line()
        