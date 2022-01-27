#prerequisites:
#git installed on windows with cmd ability
#termux installed on android
#git installed on termux
#dulwitch installed on pythons
#rclone installed on termux and configured as mobile_rclone
#google drive installed as g: on windows
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import RegexMatchingEventHandler
import shutil
import os
import sys
import getopt
from dulwich import porcelain
from datetime import datetime
import re

log_main=False
stop = False

def log(message1,*message):
    global log_main
    global path
    #print("log_main", log_main)
    if log_main:
        print(message1,message)
    else:
        if not os.path.isdir(os.path.dirname(os.path.dirname(path))+"\\log"):
            os.system("mkdir " + os.path.dirname(os.path.dirname(path))+"\\log")        
        log_file = os.path.dirname(os.path.dirname(path)) + "\\log\\auto_sync_"+os.path.basename(path)+"_console.log"
        with open(log_file,'a+') as file:
            print(message1,message,file=file)
        

def on_created(event):
    log(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    log(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    try:
        log(f"hey buddy, {event.src_path} has been modified")
        #log(aaa)
        #log(os.getcwd())
        os.chdir(path)
        log(os.getcwd())
        #log("curr dir changed")
        #os.system("git status")
        basename=os.path.basename(path)
        if os.name == 'nt':
            log("G:/My Drive/sync/company_notebook/"+basename)
            if os.path.isdir("G:/My Drive/sync/company_notebook/"+basename):
                log("its a dir")
                os.system("rd /s /q \"G:/My Drive/sync/company_notebook/"+basename+"\"")
                log("deleted")
            os.system("mkdir \"G:/My Drive/sync/company_notebook/"+basename+"\"")
            log("gdrive dir created")
            os.system("git status > \"G:/My Drive/sync/company_notebook/"+basename+"/status\"")
            log("status loged")
            os.system("git diff > \"G:/My Drive/sync/company_notebook/"+basename+"/diff\"")
            log("diff loged")
            
            repo=porcelain.open_repo(path)
            log("repo has been set")
            status=porcelain.status(repo)
            log("status got")
            log('staged - added:', status.staged['add'], 'modified:', status.staged['modify'], 'deleted: ', status.staged['delete'])     
            log('unstaged: ', status.unstaged) 
            #log 'untracked: ', status.untracked
            #untracked not working on version 0.9.7
            #log 'untracked: '+str(repo.untracked_files)
            log('untracked: ', status.untracked)
            for file in status.untracked:
                #>xcopy /s python\ftp_upload_file.pyc "G:\My Drive\sync\company_notebook\scripts\python\"
                if os.path.dirname(file) == '':
                    log(    "xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\untracked\\\"")
                    os.system("cmd.exe /c xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\untracked\\\"")
                else:
                    log(    "xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\untracked\\"+os.path.dirname(file)+"\\\"")            
                    os.system("cmd.exe /c xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\untracked\\"+os.path.dirname(file)+"\\\"")           
        else : 
            os.system("rclone purge \"mobile_rclone:/sync/private_mobile/"+basename+"\"")
            os.system("rclone mkdir \"mobile_rclone:/sync/private_mobile/"+basename+"\"")
            os.system("rclone mkdir \"mobile_rclone:/sync/private_mobile/"+basename+"/untracked\"")
            os.system("mkdir \"../"+basename+"_tmp\"")
            os.system("git status > \"../"+basename+"_tmp/status\"")
            os.system("git diff   > \"../"+basename+"_tmp/diff\"")
            os.system("rclone copy ../"+basename+"_tmp/diff   \"mobile_rclone:/sync/private_mobile/"+basename+"/\"")
            os.system("rclone copy ../"+basename+"_tmp/status \"mobile_rclone:/sync/private_mobile/"+basename+"/\"")
            os.system("rm -rf \"../"+basename+"_tmp\"")
            
            repo=porcelain.open_repo(path)
            status=porcelain.status(repo)
            log('staged - added:', status.staged['add'], 'modified:', status.staged['modify'], 'deleted: ', status.staged['delete'])     
            log('unstaged: ', status.unstaged) 
            #log 'untracked: ', status.untracked
            #untracked not working on version 0.9.7
            #log 'untracked: '+str(repo.untracked_files)
            log('untracked: ', status.untracked)
            for file in status.untracked:
                #>xcopy /s python\ftp_upload_file.pyc "G:\My Drive\sync\company_notebook\scripts\python\"
                log("rclone copy \""+file+"\" \"mobile_rclone:/sync/private_mobile/"+basename+"/untracked/"+os.path.dirname(file)+"\"")
                os.system("rclone copy \""+file+"\" \"mobile_rclone:/sync/private_mobile/"+basename+"/untracked/"+os.path.dirname(file)+"\"")
                #log(    "xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\"+os.path.dirname(file)+"\\\"")
                #os.system("xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\"+os.path.dirname(file)+"\\\"")
        
        #shutil.copy(event.src_path, "G:/My Drive/sync")
        log("ready: ", str(datetime.now()))
    except BaseException:
        os._exit(1)    
def on_moved(event):
    log(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

def observer_stop():
    global my_observer
    global stop
    my_observer.stop()
    my_observer.join()
    stop = True
    log("stopping")

def main(argv):

    ################################################### get options
    global path
    global my_observer
    global stop
    print(str(argv))
    print(len(argv))
    

    if len(argv) ==1:
        print('add parameters: ')
        params=input().split(' ')
    else:
        params=argv[1:]


    try: 
        opts, args = getopt.getopt( params ,"hp:",["help","path="])
        print('try ok')
    except getopt.GetoptError: 
        print('file_sync_to_gdrive_windows -p "path/to/git/project')
        sys.exit(2) 
        
    print('opts'+str(opts))
    print('args'+str(args))

    if len(opts) < len(args):
        print('file_sync_to_gdrive_windows -p "path/to/git/project')
        exit()    

    for opt, arg in opts: 
        if opt in ('-h','--help'): 
            print('file_sync_to_gdrive_windows -p "path/to/git/project')
            sys.exit() 
        elif opt in ("-p", "--path"): 
            path = arg
            print("incase of module log path:" + path + "\\auto_sync_console.log")
            log('path:' + path)
        else:
            print('not recognize')

    #patterns = ["*"]
    #ignore_patterns = [".*git"]
    ignore_directories = False
    case_sensitive = True
    #my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    
    regexes = [".+"]

    #ignore = ".*c:/Users/eharvin/OneDrive - Ericsson AB/000Vince/programming/git/scripts\\\\.git.*"
    #c:/Users/eharvin/OneDrive - Ericsson AB/000Vince/programming/git/scripts
    #ignore_windows = "^" + path + "\\\\.git.*"
    #ignore_regexes = [".*\\\\.git$"]
    #ignore_regexes = ["git"]
    #ignore_linux = "^" + path + "/\\.git.*"

    #ignore_regexes = [ignore_windows, ignore_linux]
    #log("ignore: " + ignore_linux)
    
    if os.name == 'nt':
        ignore = "^" + re.escape(path) + "\\\\\\.git.*"
    else:
        ignore = "^" + path + "/\\.git.*"
    
    log("ignore: " + ignore)
    ignore_regexes = [ignore]    
    
    my_event_handler = RegexMatchingEventHandler (regexes=regexes,ignore_regexes=ignore_regexes, ignore_directories=ignore_directories, case_sensitive=case_sensitive)
    

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)    

    my_observer.start()
    try:
        while True:
            time.sleep(1)
            if stop:
                break
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
        
if __name__ == "__main__":
    log_main = True
    main(sys.argv)
    
    
