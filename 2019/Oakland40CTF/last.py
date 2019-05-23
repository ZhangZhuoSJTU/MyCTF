#!/usr/bin/env python
# coding=utf-8


f = file("./input")
out = ""
for line in f:
    line = line.strip()
    out += chr(int(line))

print out

