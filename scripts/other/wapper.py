#! /usr/bin/python3
import os
import sys
import select

def log_into_file(buffer):
	with open('./log','a+') as f:
		f.write(buffer)

class Fuzzer(object):
    def __init__(self,target,args=""):
        self.target = target
        self.args = args

    def fflush(self):
        sys.stdin.flush()
        sys.stdout.flush()
        sys.stderr.flush()

    def createPipe(self):
        self.pipe1 = os.pipe()
        self.pipe2 = os.pipe()
    
    def getChild(self):
        return os.fork()

    def childWork(self):
        os.close(self.pipe1[1])            # pipe 1 write
        os.close(self.pipe2[0])            # pipe 2 read
        os.dup2(self.pipe1[0],0)   		   # pipe 1 read
        os.dup2(self.pipe2[1],1) 		   # pipe 2 write
        if self.args != "":
            os.execvp(self.target,[self.target,self.args])
        else:
            os.execvp(self.target,[self.target])

        sys.exit()

    def fatherWork(self,pid):
        os.close(self.pipe1[0])
        os.close(self.pipe2[1])

        while True:
            self.fflush()
            inputs = [sys.stdin , self.pipe2[0]]
            outputs = []
            msg_queues = {}
            timeout = 10
            readable,writeable,exceptional = select.select(inputs, outputs, inputs, timeout)
            if not (readable or writeable or exceptional):
                print ("[*]Timeout !")
                break
            for s in readable:
                if s is sys.stdin:
                    buffer = os.read(0,1024)
                    os.write(self.pipe1[1],buffer)
                    log_into_file(buffer)
                    self.fflush()
                elif s is self.pipe2[0]:
                    buffer = os.read(self.pipe2[0],1024)
                    os.write(1,buffer)
                    log_into_file(buffer)
                    self.fflush()
        os.waitpid(pid,0)
        
    def exploit(self):
        self.createPipe()
        pid = self.getChild()
        if pid == 0:
            self.childWork()
        elif pid > 0:
            self.fatherWork(pid)
        else:
            print ("[*]Fork Error!")

def main():
    f = Fuzzer('./target')
    f.exploit()

if __name__ == '__main__':
    main()