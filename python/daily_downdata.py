from zipfile import ZipFile
import sys
import getopt
import glob
import os
import os.path


BUFSIZE = 1024

def are_equivalent(filename1, filename2):
    """Compare two ZipFiles to see if they would expand into the same directory structure
    without actually extracting the files.
    """
    
    with ZipFile(filename1, 'r') as zip1, ZipFile(filename2, 'r') as zip2:
        
        # Index items in the ZipFiles by filename. For duplicate filenames, a later
        # item in the ZipFile will overwrite an ealier item; just like a later file
        # will overwrite an earlier file with the same name when extracting.
        zipinfo1 = {info.filename:info for info in zip1.infolist()}
        zipinfo2 = {info.filename:info for info in zip2.infolist()}
        
        # Do some simple checks first
        # Do the ZipFiles contain the same the files?
        if zipinfo1.keys() != zipinfo2.keys():
            return False
        
        # Do the files in the archives have the same CRCs? (This is a 32-bit CRC of the
        # uncompressed item. Is that good enough to confirm the files are the same?)
        if any(zipinfo1[name].CRC != zipinfo2[name].CRC for name in zipinfo1.keys()):
            return False
        
        # Skip/omit this loop if matching names and CRCs is good enough.
        # Open the corresponding files and compare them.
        for name in zipinfo1.keys():
            
            # 'ZipFile.open()' returns a ZipExtFile instance, which has a 'read()' method
            # that accepts a max number of bytes to read. In contrast, 'ZipFile.read()' reads
            # all the bytes at once.
            with zip1.open(zipinfo1[name]) as file1, zip2.open(zipinfo2[name]) as file2:
                
                while True:
                    buffer1 = file1.read(BUFSIZE)
                    buffer2 = file2.read(BUFSIZE)
                    
                    if buffer1 != buffer2:
                        return False
                    
                    if not buffer1:
                        break
                        
        return True
        
#get path parameter
#list path and get all database.zip file
#get the last 2 one
#compare them

#delete new one if its same as the old one
#delete oldest one if its different and there are more than 3 file

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if len(sys.argv) ==1:
    print('add parameters: ')
    params=input().split(' ')
else:
    params=sys.argv[1:]


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
        print('path:' + path)
    else:
        print('not recognize')

os.chdir(path)
print('cwd_script:',os.getcwd())

list_of_files = glob.glob('*database.zip')
if len(list_of_files) > 2:   
    print(list_of_files[-1],list_of_files[-2])
    print(are_equivalent(list_of_files[-1],list_of_files[-2]))
    if are_equivalent(list_of_files[-1],list_of_files[-2]):
        os.remove(list_of_files[-1])
    elif len(list_of_files) > 3:
        os.remove(list_of_files[0])
