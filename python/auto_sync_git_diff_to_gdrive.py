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

def on_created(event):
    print(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    try:
        print(f"hey buddy, {event.src_path} has been modified")
        #print(os.getcwd())
        os.chdir(path)
        print(os.getcwd())
        #print("curr dir changed")
        #os.system("git status")
        basename=os.path.basename(path)
        if os.name == 'nt':
            print("G:/My Drive/sync/company_notebook/"+basename)
            if os.path.isdir("G:/My Drive/sync/company_notebook/"+basename):
                print("its a dir")
                os.system("rd /s /q \"G:/My Drive/sync/company_notebook/"+basename+"\"")
                print("deleted")
            os.system("mkdir \"G:/My Drive/sync/company_notebook/"+basename+"\"")
            os.system("git status > \"G:/My Drive/sync/company_notebook/"+basename+"/status\"")
            os.system("git diff > \"G:/My Drive/sync/company_notebook/"+basename+"/diff\"")
            
            repo=porcelain.open_repo(path)
            status=porcelain.status(repo)
            print('staged - added:', status.staged['add'], 'modified:', status.staged['modify'], 'deleted: ', status.staged['delete'])     
            print('unstaged: ', status.unstaged) 
            #print 'untracked: ', status.untracked
            #untracked not working on version 0.9.7
            #print 'untracked: '+str(repo.untracked_files)
            print('untracked: ', status.untracked)
            for file in status.untracked:
                #>xcopy /s python\ftp_upload_file.pyc "G:\My Drive\sync\company_notebook\scripts\python\"
                if os.path.dirname(file) == '':
                    print(    "xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\untracked\\\"")
                    os.system("xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\untracked\\\"")
                else:
                    print(    "xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\untracked\\"+os.path.dirname(file)+"\\\"")            
                    os.system("xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\untracked\\"+os.path.dirname(file)+"\\\"")           
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
            print('staged - added:', status.staged['add'], 'modified:', status.staged['modify'], 'deleted: ', status.staged['delete'])     
            print('unstaged: ', status.unstaged) 
            #print 'untracked: ', status.untracked
            #untracked not working on version 0.9.7
            #print 'untracked: '+str(repo.untracked_files)
            print('untracked: ', status.untracked)
            for file in status.untracked:
                #>xcopy /s python\ftp_upload_file.pyc "G:\My Drive\sync\company_notebook\scripts\python\"
                print("rclone copy \""+file+"\" \"mobile_rclone:/sync/private_mobile/"+basename+"/untracked/"+os.path.dirname(file)+"\"")
                os.system("rclone copy \""+file+"\" \"mobile_rclone:/sync/private_mobile/"+basename+"/untracked/"+os.path.dirname(file)+"\"")
                #print(    "xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\"+os.path.dirname(file)+"\\\"")
                #os.system("xcopy /s \""+file+"\" \"G:\\My Drive\\sync\\company_notebook\\"+basename+"\\"+os.path.dirname(file)+"\\\"")
        
        #shutil.copy(event.src_path, "G:/My Drive/sync")
        print("ready: ", datetime.now())
    except BaseException:
        os._exit(1)    
def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


if __name__ == "__main__":

    ################################################### get options

    print(str(sys.argv))
    print(len(sys.argv))

    if len(sys.argv) ==1:
        print('add parameters: ')
        params=input().split(' ')
    else:
        params=sys.argv[1:]


    try: 
        opts, args = getopt.getopt( params ,"p:",["path="])
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
            print('path:' + path)
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
    #print("ignore: " + ignore_linux)
    
    if os.name == 'nt':
        ignore = "^" + re.escape(path) + "\\\\\\.git.*"
    else:
        ignore = "^" + path + "/\\.git.*"
    
    print("ignore: " + ignore)
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
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
