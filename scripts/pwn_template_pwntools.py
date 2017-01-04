from pwn import *

context.log_level = 'debug'
#context.arch=''

LOCAL = True

if LOCAL:
	p = process('filename')
else:
	p = remote('127.0.0.1',10001)



def main():
    p.interactive()

if __name__ == '__main__':
	main()
