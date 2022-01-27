import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import shutil
import sys
import os
import os.path
from datetime import datetime
import getpass

def log(message1,*message):
    global log_main
    global path
    #print("log_main", log_main)
    if log_main:
        print(message1,message)
    else:
        if not os.path.isdir("C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\log"):
            os.system("mkdir C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\log")        
        log_file = "C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\log\\kisokos_sync_console.log"
        with open(log_file,'a+') as file:
            print(message1,message,file=file)

def on_created(event):
    log(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    log(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    log(f"hey buddy, {event.src_path} has been modified")
    #log("before")
    #log(      "cmd.exe /c xcopy /Y \"" +event.src_path+ "\" \"G:\\My Drive\\company\\\" >> \"C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\log\\kisokos_sync_console.log\"")
    #os.system("cmd.exe /c xcopy /Y \"" +event.src_path+ "\" \"G:\\My Drive\\company\\\" >> \"C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\log\\kisokos_sync_console.log\"")
    shutil.copy(event.src_path, "G:/My Drive/company/")
    #log("after")
    #log(      "rclone copy \"" +event.src_path+ "\" \"hvgd:/company/\" -P >> \"C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\log\\kisokos_sync_console.log\"")
    #os.system("rclone copy \"" +event.src_path+ "\" \"hvgd:/company/\" -P >> \"C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\log\\kisokos_sync_console.log\"")
    #os.system("echo szatyor >> \"C:\\Users\\eharvin\\OneDrive - Ericsson AB\\000Vince\\programming\\log\\kisokos_sync_console.log\"")
    log("ready: ", str(datetime.now()))

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
    global my_observer
    global stop
    log("user:", getpass.getuser())
    patterns = ["*kisokos.txt"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = "c:\\Users\\eharvin\\OneDrive - Ericsson AB\\00company"
    go_recursively = False
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


stop = False

if __name__ == "__main__":
    log_main = True
    main(sys.argv)
else:
    log_main=False
    