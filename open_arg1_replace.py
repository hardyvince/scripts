import sys
import re
fullFile = ''
file = open(sys.argv[1],'r')
for line in file:
	fullFile += line
fullFile = re.sub("foo","bar",fullFile)
print fullFile
