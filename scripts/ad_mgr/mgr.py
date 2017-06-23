#!/usr/bin/python2
from pwn import *
import xml.etree.ElementTree as ET
import sys 
import subprocess
import requests
import random

'''
author : muhe@Syclover
For CTF AWD Mode to manage server.
'''

#context.log_level = 'Debug'

server_xml  = "./server.xml"
server_list = []


CHECK_LOCAL = 1
CHECK_SCRIPT = 2
CHECK_ALL_WAYS = 3

default_local_path = "/home/muhe/Desktop/ad_pwn_mgr/"
default_local_filename = "checker.py"
default_remote_path = "/root/"
default_remote_filename = "checker.py"

server_path = "/root/"
server_name = "pwn"


#flag_for_check_down = 1

USER_AGENTS = [
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
  "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
  "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
  "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
  "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
  "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
  "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

def random_useragent(condition=False):
  if condition:
    return random.choice(USER_AGENTS)
  else:
    return USER_AGENTS[0]

def gn1(io,room):
    io.recvuntil('6.Chi tang',timeout=5)
    io.sendline('1')
    io.recvuntil('Give me the class room name',timeout=5)
    io.sendline(str(room))
    io.recvuntil('success')

def gn2(io,room):
    io.recvuntil('6.Chi tang',timeout=5)
    io.sendline('1')
    io.recvuntil('Give me the class room name',timeout=5)
    io.sendline(str(room))
    io.recvuntil('success')

def gn3(io,room):
    io.recvuntil('6.Chi tang',timeout=5)
    io.sendline('1')
    io.recvuntil('Give me the class room name',timeout=5)
    io.sendline(str(room))
    io.recvuntil('success')

def gn4(io,name):
    io.recvuntil('6.Chi tang',timeout=5)
    io.sendline('4')
    io.recvuntil('Your must have a book card first',timeout=5)
    io.sendline('y')
    io.recvuntil('Input your name',timeout=5)
    io.sendline(name)
    io.recvuntil('success')

def gn5(io,message):
    io.recvuntil('6.Chi tang',timeout=5)
    io.sendline('5')
    io.recvuntil('where do you want to go?',timeout=5)
    io.sendline('6602')
    io.recvuntil('your can leave some message to us',timeout=5)
    io.sendline(message)

def gn6(io):
    io.recvuntil('6.Chi tang',timeout=5)
    io.sendline('6')


class Checker_ad(object):
    def __init__(self, host,port):
        self.host = host
        self.port = port
        self.io = remote(self.host,port)
    
    def __del__(self):
        self.io.close()
    
    def gn1(room):
        self.io.recvuntil('6.Chi tang')
        self.io.sendline('1')
        self.io.recvuntil('Give me the class room name')
        self.io.sendline(str(room))

    def gn2(room):
        self.io.recvuntil('6.Chi tang')
        self.io.sendline('1')
        self.io.recvuntil('Give me the class room name')
        self.io.sendline(str(room))

    def gn3(room):
        self.io.recvuntil('6.Chi tang')
        self.io.sendline('1')
        self.io.recvuntil('Give me the class room name')
        self.io.sendline(str(room))

    def gn4(name):
        self.io.recvuntil('6.Chi tang')
        self.io.sendline('4')
        self.io.recvuntil('Your must have a book card first')
        self.io.sendline('y')
        self.io.recvuntil('Input your name')
        self.io.sendline(name)

    def gn5(message):
        self.io.recvuntil('6.Chi tang')
        self.io.sendline('5')
        self.io.recvuntil('where do you want to go?')
        self.io.sendline('6602')
        self.io.recvuntil('your can leave some message to us')
        self.io.sendline(message)

    def gn6():
        self.io.recvuntil('6.Chi tang')
        self.io.sendline('6')

    def docheck(self):
        try:
            self.gn1('aafdaa')
            self.gn2('aaafdsa')
            self.gn3('aaaaa ogogo')
            self.gn4('lemon dsb')
            self.gn5('hacked by master go')
            self.gn6()
            self.io.close()
            return 1
        except Exception,e:
            return -1
            

class Checker(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.p = remote(self.host,self.port)

    def func_1(self):
        self.p.recvuntil("choice:",timeout=10)
        self.p.sendline("1")

    def func_2(self):
        self.p.recvuntil("choice:",timeout=10)
        self.p.sendline("2")

    def func_3(self):
        self.p.recvuntil("choice:",timeout=10)
        self.p.sendline("3")

    def func_4(self):
        self.p.recvuntil("choice:",timeout=10)
        self.p.sendline("4")

    def docheck(self):
        try:
            self.func_1()
            self.func_2()
            self.func_3()
            self.func_4()
            return 1
        except Exception,e:
            return -1

    def __del__(self):
        self.p.close()


class Server(object):
    def __init__(self,host,port,username,password):
        self.host = host
        self.port = int(port,10)
        self.username = username
        self.password = password
        self.sh = self.__connect__()

    def __del__(self):
        self.sh.close()
        
    def __connect__(self):
        try:
            sh = ssh(host=self.host,port=self.port,user=self.username,password=self.password)
            print '[*]Connected!'
            return sh
        except Exception,e:
            print "[!] : Connect Error!"

    def __disconnect__(self):
            print "See you again"
            self.sh.close()

    def __check__(self,service_id=CHECK_ALL_WAYS):
            ret = self.sh.run_to_end('python /root/checker.py '+server_path+server_name)
            print ret
            if ret[1] == -1:
                return False
            else:
                return True

    def __interactive__(self):
        self.sh.interactive()

    def __uploadfile__(self,local_path,local_filename,remote_path,remote_filename):
        #eg:
        #local:/home/muhe/testfile
        #remote:/home/pwn/
        #upload_file("/home/muhe/","testfile","/home/pwn/","new_name")
        try:
            self.sh.upload_file(local_path+local_filename,remote_path+remote_filename)
        except Exception ,e:
            print "Upload file error"

    def __downloadfile__(self,remote_path,remote_filename,local_path,local_filename):
        try:
            self.sh.download_file(remote_path+remote_filename,local_path+local_filename)
        except Exception,e:
            print "Download file error"

    def __runcmd__(self,cmd):
        try:
            self.sh.run_to_end(cmd)
        except Exception,e:
            print "Execute cmd error"

def my_raw_input(arg):
    __ioflush__()
    print arg
    return raw_input()


def check_down(ip):
    
    url = "http://checker?id={0}".format(ip)
    header = {
      'User-Agent': random_useragent(True)
    }
    r = requests.get(url,headers=header)
    print r.url
    print "\n[*]response: %d " % r.status_code 
    
    print "[*]down : {0}".format(ip)


def __parseXmlfile():
    global server_list
    tmp_dic = {"Host":"","Port":"","Username":"","Password":""}
    try: 
        tree = ET.parse(server_xml)
        root = tree.getroot()
        for elem in root.findall('Serverinfo'):
            tmp_dic["Host"] = elem.find('Host').text
            tmp_dic["Port"] = elem.find('Port').text
            tmp_dic["Username"] = elem.find('Username').text
            tmp_dic["Password"] = elem.find('Password').text
            server_list.append(tmp_dic.copy())
    except Exception,e: 
        print "Error:cannot parse file:%s" % server_xml

def __getServer__():
    __parseXmlfile()

def __menu__():
    print "\t1. Check All Servers"
    print "\t2. Upload file by id"
    print "\t3. Download file by id"
    print "\t4. Upload file to all Server"
    print "\t5. Download file from all Server"
    print "\t6. Shell to interactive"
    print "\t7. Execute cmd(to all server)"
    print "\t8. Exit"
    print ""

check_round = 1
def __checkAll__():
    #__checkFile__()
    global check_round
    while True:
        print "\t====check round %d====" % check_round
        __checkInteract__()
        __ioflush__()
        sleep(600)
        check_round += 1

'''
def __checkFile__():
    global flag_for_check_down
    print "Checking All Servers..."
    #for server 
    print "Checker 1 is running..."
    for idx in xrange(0,len(server_list)):
        try:
            server = Server(server_list[idx]["Host"],server_list[idx]["Port"],server_list[idx]["Username"],server_list[idx]["Password"])
            if(server.__check__()):
                print "[*]Server %d is ok" % idx
            else:
                print "[!]Server %d replace" % idx
                if flag_for_check_down > 0:
                    check_down(server_list[idx]["Host"])
                    flag_for_check_down -= 1
        except Exception,e:
            print "[!]Unknow error,plz debug"
            if flag_for_check_down > 0:
                check_down(server_list[idx]["Host"])
                flag_for_check_down -= 1
        if flag_for_check_down == 0:
            flag_for_check_down = 1
'''

def __checkInteract__():
    #interact 
    global flag_for_check_down
    for idx in xrange(0,len(server_list)):
        try:
            '''
            io = remote(server_list[idx]["Host"],server_list[idx]["Port"],timeout=5)
            gn1(io,'aaa')
            gn2(io,'bbb')
            gn3(io,'ccc')
            gn4(io,'ddd')
            gn5(io,'eee')
            gn6(io)
            io.close()
            '''
            cmdline = "python exp.py {0} {1}".format(server_list[idx]["Host"],23333)
            #print cmdline
            ret = subprocess.call(cmdline,shell=True)
            print "ret:%d" % ret
            if ret == 2:
                print "[*]Server %d is shut" % idx
                check_down(server_list[idx]["Host"])
            else:
                print "[*]Server %s is  ok" % server_list[idx]["Host"]
            print ""
        except Exception,e:
            print "[!]unknow error,plz debug %s" % server_list[idx]["Host"]

def __uploadfile__():
    print "Which server you want to upload file:"
    for idx in xrange(0,len(server_list)):
        print "%d. %s" % (idx,server_list[idx]["Host"])
    opt = int(my_raw_input("Which server you want to upload file:"),10)
    if(opt < 0 or opt > (len(server_list)+1)):
        print "Are you kidding me?"
    else:
        server = Server(server_list[opt]["Host"],server_list[opt]["Port"],
                    server_list[opt]["Username"],server_list[opt]["Password"])
        server.__uploadfile__(default_local_path,default_local_filename,
                    default_remote_path,default_remote_filename)


def __downloadfile__():
    print "Which server you want to download file from:"
    for idx in xrange(0,len(server_list)):
        print "%d. %s" % (idx,server_list[idx]["Host"])
    opt = int(my_raw_input("Which server you want to upload file:"),10)
    if(opt < 0 or opt > (len(server_list)+1)):
        print "Are you kidding me?"
    else:
        server = Server(server_list[opt]["Host"],server_list[opt]["Port"],
                server_list[opt]["Username"],server_list[opt]["Password"])
        server.__downloadfile__(default_remote_path,default_remote_filename,
                default_local_path,default_local_filename)

def __uploadfileAll__():
    print "Upload file to all server"
    print "\t1. Default mode"
    print "\t2. Custom mode"
    opt = int(my_raw_input("\tPlz choose:"),10)
    if(opt == 1):
        for idx in xrange(0,len(server_list)):
            server = Server(server_list[idx]["Host"],server_list[idx]["Port"],
                        server_list[idx]["Username"],server_list[idx]["Password"])
            server.__uploadfile__(default_local_path,default_local_filename,
                        default_remote_path,default_remote_filename)
            print "All done"
    elif(opt == 2):
        __ioflush__()
        local_path = my_raw_input("\t[-]local_path:").strip()
        local_filename = my_raw_input("\t[-]local_filename:").strip()
        remote_path = my_raw_input("\t[-]remote_path:").strip()
        remote_filename = my_raw_input("\t[-]remote_filename:").strip()
        print "local:%s" % local_path + local_filename
        print "remote:%s" % remote_path + remote_filename
        for idx in xrange(0,len(server_list)):
            server = Server(server_list[idx]["Host"],server_list[idx]["Port"],
                        server_list[idx]["Username"],server_list[idx]["Password"])
            server.__uploadfile__(local_path,local_filename,
                        remote_path,remote_filename)
            print "All done"


def __downloadfileAll__():
    print "Download file from all server"
    for idx in xrange(0,len(server_list)):
        server = Server(server_list[idx]["Host"],server_list[idx]["Port"],
                        server_list[idx]["Username"],server_list[idx]["Password"])
        server.__downloadfile__(default_remote_path,default_remote_filename,
                             default_local_path,default_local_filename+"_server"+str(idx))
    print "All done"

def __shell__():
    for idx in xrange(0,len(server_list)):
        print "%d. %s" % (idx,server_list[idx]["Host"])
    opt = int(my_raw_input("Plz choice the server you want:"),10)
    if(opt < 0 or opt > (len(server_list)-1)):
        print "Are you kidding me?"
    else:
        server = Server(server_list[opt]["Host"],server_list[opt]["Port"],
                       server_list[opt]["Username"],server_list[opt]["Password"])
        server.__interactive__()

def __executecmd__():
    cmd = my_raw_input("plz input your cmd:")
    for idx in xrange(0,len(server_list)):
        server = Server(server_list[idx]["Host"],server_list[idx]["Port"],
                        server_list[idx]["Username"],server_list[idx]["Password"])
        server.__runcmd__(cmd)

def __ioflush__():
    sys.stdin.flush()
    sys.stdout.flush()
    sys.stderr.flush()


def main():
    print "\t\tWelcome to Syclover AD-PWN Manger"
    __getServer__()
    while True:
        __ioflush__()
        __menu__()
        opt = int(my_raw_input("Plz input your choice:"),10)
        if opt == 1:
            __checkAll__()
        elif opt == 2:
            __uploadfile__()
        elif opt == 3:
            __downloadfile__()
        elif opt == 4:
            __uploadfileAll__()
        elif opt == 5:
            __downloadfileAll__()
        elif opt == 6:
            __shell__()
        elif opt == 7:
            __executecmd__()
        elif opt == 8:
            sys.exit(1)
        else:
            print "Error"


if __name__ == '__main__':
    main()
