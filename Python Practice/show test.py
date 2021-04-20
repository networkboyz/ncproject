import paramiko
import time
import datetime
import os
network_devices = ['192.168.52.101']

IP  = input('[+] IP: ')
UN = 'alex'
PW = 'alex'

for ip in  network_devices:
    print ('Trying to establish SSH connection into ' + ip)
    twrssh = paramiko.SSHClient()
    twrssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    twrssh.connect(ip, port=22, username=UN, password=PW)
    remote = twrssh.invoke_shell()
    remote.send('term len 0\n')
    time.sleep(1)

    remote.send('show int desc\n')
    time.sleep(2)

    buf = remote.recv(65000)
    print (buf)
    #time.sleep(2)
    #f = open('sshlog'+ str(datetime.datetime.now()) + '.txt', 'a')
    f = open(str(IP) +  '.txt', 'wb')

    f.write(buf)
    f.close()
    twrssh.close()

a =  input('[-] Press enter to exit')

