# -*- coding: utf-8 -*-
#!/usr/bin/env python2
from pwn import *
import sys

#context.log_level = 'debug'
context.arch = 'amd64'


def gn1(io,room):
    data = io.recvuntil('6.Chi tang',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline('1')
    data = io.recvuntil('Give me the class room name',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline(str(room))
    io.recvuntil('success')

def gn2(io,room):
    data = io.recvuntil('6.Chi tang',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline('1')
    data = io.recvuntil('Give me the class room name',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline(str(room))
    io.recvuntil('success')

def gn3(io,room):
    data = io.recvuntil('6.Chi tang',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline('1')
    data = io.recvuntil('Give me the class room name',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline(str(room))
    io.recvuntil('success')

def gn4(io,name):
    data = io.recvuntil('6.Chi tang',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline('4')
    data = io.recvuntil('Your must have a book card first',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline('y')
    io.recvuntil('Input your name')
    io.sendline(name)
    io.recvuntil('success')

def gn5(io,message):
    data = io.recvuntil('6.Chi tang',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline('5')
    data = io.recvuntil('where do you want to go?',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline('6602')
    data = io.recvuntil('your can leave some message to us',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline(message)

def gn6(io):
    data = io.recvuntil('6.Chi tang',timeout=10)
    #log.info("data:{0}".format(data))
    if data == "":
        sys.exit(2)
    io.sendline('6')

def main():
    try:
        io = remote(sys.argv[1],sys.argv[2],timeout=10)
        gn1(io,'aaa')
        gn2(io,'bbb')
        gn3(io,'ccc')
        gn4(io,'ddd')
        gn5(io,'eee')
        gn6(io)
        io.close()
        sys.exit(1)
    except Exception,e:
        sys.exit(2)

   
if __name__ == '__main__':
    main()
