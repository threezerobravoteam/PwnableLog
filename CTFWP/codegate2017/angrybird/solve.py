#!/usr/bin/env python
# coding=utf-8

import angr


start_addr = 0x00000000004007C2

def main():
    prog = angr.Project('angrybird', load_options={"auto_load_libs": False}) 

    #s = prog.factory.entry_state(addr=start_addr)
    s = prog.factory.blank_state(addr=start_addr)
    path = prog.factory.path(s)
    pg = prog.factory.path_group(path, immutable=False)

    find = pg.explore(find=(0x0000000000404FC1))

    print find
    print pg.found[-1].state.posix.dumps(0) 

if __name__ == '__main__':
    main()

