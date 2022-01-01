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
    opts, args = getopt.getopt( params ,"hc:k:",["help","cypher=","key="])
    print('try ok')
except getopt.GetoptError: 
    print('decrypt_password.py -c <cypher> -k <key>') 
    sys.exit(2) 
    
print('opts'+str(opts))
print('args'+str(args))

if len(opts) < len(args):
    print('decrypt_password.py -c <cypher> -k <key>') 
    exit()    

for opt, arg in opts: 
    if opt in ('-h','--help'): 
        print('decrypt_password.py -c <cypher> -k <key>') 
        sys.exit() 
    elif opt in ("-c", "--cypher"): 
        cypher = arg
        print('cypher:' + cypher)
    elif opt in ("-k", "--key"): 
        key = arg
        print('key: '+ key)
    else:
        print('not recognize')


b_cypher=base64.b64decode(cypher)
B_key=bytes(key,'ascii')
d=bytearray()
for i in range(len(b_cypher)):
     d.append(b_cypher[i]-B_key[i%len(B_key)])
print(d.decode('ascii'))
