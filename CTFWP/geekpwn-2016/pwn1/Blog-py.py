import time
import os
import sys
class flushfile(object):
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()
sys.stdout = flushfile(sys.stdout)
def gen_id():
    now = int(time.time())
    return '%d.em' % now
def list_blog():
    l = []
    f = open('bloglist.txt', 'r')
    l = [ x.strip() for x in f ]
    f.close()
    return l
def write_blog():
    content = raw_input('Please input blog content: \n')
    filename = gen_id()
    fw = open(filename, 'a+')
    fw.write(content)
    fw.close()
    while True:
        try:
            f = open('bloglist.txt', 'a+')
            break
        except:
            pass
    f.write(filename + '\n')
    f.close()
def read_blog():
    filename = raw_input('Please input blog name: \n')
    filename = filename.strip()
    if filename not in list_blog():
        if not os.path.exists(filename):
            print 'File not exist!'
            return
    fr = open(filename, 'r')
    content = fr.read()
    fr.close()
    print content
def menu():
    print '---- UAV Pilot Blog Version 2.0 ----'
    print '   1. List Blog'
    print '   2. Write Blog'
    print '   3. Read Blog'
    print '   4. Exit'
    print '------------------------------------'
    return raw_input('Your choice: \n')
def main():
    choice = int(menu())
    if choice == 1:
        print '-- File List --'
        for x in list_blog():
            print x
        print '---------------'
    if choice == 2:
        write_blog()
    if choice == 3:
        read_blog()
    if choice == 4:
        exit()
if __name__ == '__main__':
    os.chdir('/home/muhe/geekpwn-2016/pwn1/')
    while True:
        main()