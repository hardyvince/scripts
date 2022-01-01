import getopt
import sys
import base64

################################################### get options

print(str(sys.argv))
print(len(sys.argv))

if len(sys.argv) ==1:
    print('add parameters: ')
    params=input().split(' ')
else:
    params=sys.argv[1:]


try: 
    opts, args = getopt.getopt( params ,"hp:k:",["help","password=","key="])
    print('try ok')
except getopt.GetoptError: 
    print('encrypt_password.py -p <password> -k <key>') 
    sys.exit(2) 
    
print('opts'+str(opts))
print('args'+str(args))

if len(opts) < len(args):
    print('encrypt_password.py -p <password> -k <key>') 
    exit()    

for opt, arg in opts: 
    if opt in ('-h','--help'): 
        print('encrypt_password.py -p <password> -k <key>') 
        sys.exit() 
    elif opt in ("-p", "--password"): 
        password = arg
        print('password:' + password)
    elif opt in ("-k", "--key"): 
        key = arg
        print('key: '+ key)
    else:
        print('not recognize')




B_key=bytes(key,'ascii')
B_password=bytes(password,'ascii')
e=bytearray()
for i in range(len(B_password)):
     e.append(B_key[i%len(B_key)]+B_password[i])
print(base64.b64encode(e))

