from zio import *


LOCAL = True

if LOCAL:
    target = './filename'
else:
    target = ('127.0.0.1',10001)

io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))


def main():
    io.interact()

if __name__ =='__main__':
    main()
