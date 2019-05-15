import ftplib  
session = ftplib.FTP([ftp_server_addr],[username],[password]) 
session.cwd([directory])

fileName=[path]	
file = open( fileName ,'rb') # file to send 
print fileName

# send the file
session.storbinary('STOR '+fileName, file) 

# close file and FTP
file.close()
session.quit()
