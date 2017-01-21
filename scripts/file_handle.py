#!/usr/bin/env python
# coding=utf-8
# by muhe@Syclover
# for CTF-AD model

from pwn import *
import getopt, sys

#connect info
default_host = ""
default_port = 22
default_user = "user-name-here"
default_pwd  = "pwd-here"

#file info
upload_file = ""
download_file = ""
local_file_path = ""
remote_file_path = ""

#remote info
bin_path = "/home/username/"
#
patch_count = 0
backup_count = 0

class Conn:
	global bin_path
	def __init__(self,host,port,username,password):
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.sh = self.get_conn()

	def get_conn(self):
	    try:
	        sh = ssh(host=self.host,port=self.port,user=self.username,password=self.password)
	        print '[SYC]Connected!'
	        return sh
	    except Exception,e:
	        print "[!!!] : " + str(e)

	def upload_file_new(self,local_path,local_file_name,remote_path=bin_path):
		self.sh.upload_file(local_path + local_file_name,remote_path + local_file_name)
		self.set_privilege(remote_path,local_file_name)

	def download_file(self,local_path,remote_path,remote_file_name):
	   	self.sh.download_file(remote_path+remote_file_name,local_path+"download-syc")

	def set_privilege(self,remote_path,remote_filename):
	    print "chmod a+x"
	    self.sh['chmod a+x ' +" "+ remote_path + remote_filename]

	def close_conn(self):
		self.sh.close()

	def conn_interact(self):
		return self.sh.interactive()
def Usage():
	print "Usage:"
	print "1. upload file to server:"
	print "python %s -l local_path [-r remote_path] -u local_file_name" % (sys.argv[0])
	'''
	python file_handle.py -u testfile -l ~/Desktop/syc_pwn_handle/ -r /tmp/
	python file_handle.py -u testfile -l ~/Desktop/syc_pwn_handle/
	'''
	print "2. download file from server:"
	print "python %s -l local_path -r remote_path -d remote_file_name" % (sys.argv[0])
	'''
	python file_handle.py -d testfile -r /home/muhe/ -l ~/Desktop/
	'''

def main():
	global upload_file
	global download_file
	global local_file_path
	global remote_file_path
	try:
		options,args = getopt.getopt(sys.argv[1:],"hu:d:r:l:",["help","upload=","download=","localpath=","remotepath"])
	except getopt.GetoptError,e:
		print "[!!!]" + str(e)
		sys.exit(1)
	for op,value in options:
		if op in ('-h','--help'):
			Usage()
			sys.exit(1)
		elif op in ('--upload'):
			upload_file = value
		elif op in ('--download'):
			download_file = value
		elif op in ('--localpath'):
			local_file_path = value
		elif op in ('--remotepath'):
			remote_file_path = value
		else:
			print "[!!!]Invalid option!"
			sys.exit(1)
	connect = Conn(default_host,default_port,default_user,default_pwd)
	
	if((upload_file!="") and (local_file_path!="")):
		if(remote_file_path!=""):
			connect.upload_file_new(local_file_path,upload_file,remote_file_path)
		else:
			connect.upload_file_new(local_file_path,upload_file)

	elif((download_file!="") and (local_file_path!="") and (remote_file_path!="")):
		connect.download_file(local_file_path,remote_file_path,download_file)

	connect.conn_interact()
if __name__ == '__main__':
    main()
