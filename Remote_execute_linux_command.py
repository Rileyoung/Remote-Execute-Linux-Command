# Script Name		: Remote_execute_linux_command.py
# Author				: Riley Young
# Created				: 25th November 2016
# Last Modified	:
# Version				: 1.0
# Modifications	:

# Description			: run linux command ,upload and download fiels using ssh through remote host. 

#!/usr/bin/python
#coding:utf-8
import paramiko
from fabric.api import env,put,get
import threading

class Host:
    def __init__(self,ip,user,password):
        self.user=user
        self.ip=ip
        self.password=password

    def run(self,cmd):
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip,username=self.user,password=self.password)
            for m in cmd:
                stdin,stdout,stderr=ssh.exec_command(m)
                print stdout.read()
            print "Check Status: %s\tOK\n"%(self.ip)
            ssh.close()
        except:
            print "%s\tError\n"%(self.ip)

    def mkdir(self):
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip,username=self.user,password=self.password)
            sftp = ssh.open_sftp()
            sftp.mkdir("security_check")
            print "Create folder 'security_check' in remote hosts successfully!\n"
            ssh.close()
        except:
            print "Create folder failure!\n"

    def upload(self,uSRC,uDST):
        env.user=self.user
        env.password=self.password
        env.host_string=self.ip
        put("%s" %(uSRC),"%s" %(uDST))
        print "Upload local file : \"%s\" to Host : %s \"%s\"\n" %(uSRC,self.ip.split(':')[0],uDST)

    def download(self,dSRC,dDST):
        env.user=self.user
        env.password=self.password
        env.host_string=self.ip
        get("%s" %(dSRC),"%s" %(dDST))
        print "Download remote file from : \"%s\" to : %s \"%s\"\n" %(dDST,self.ip.split(':')[0],dSRC)

if __name__ == '__main__':
    t=Host("192.168.142.131","root","password")
    print "Begin......\n"
    t.mkdir()
    t.upload("/root/1.txt","/root/test")
    t.download("/root/0920/2.txt","/root/2.txt")
    cmd = ["cal","ls","rm -rf /root/1.txt"]
    t.run(cmd)
