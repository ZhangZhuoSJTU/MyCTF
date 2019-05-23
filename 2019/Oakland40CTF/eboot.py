#!/usr/bin/env python
# coding=utf-8

original_matrix = [0x29B, 0x2A8, 0x2B1, 0x2BE, 0x2A0, 0x2B1, 0x2BE, 0x2A1, 0x2B4, 0x2A6, 0x29E, 0x2A8]

check_matrix = [0x29B, 0x2A8, 0x2B1, 0x2BE, 0x2A0, 0x2B1, 0x2BE, 0x2A1, 0x2B4, 0x2A6, 0x29E, 0x2A8]

mix_table = {1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 7, 7: 8, 8: 6, 9: 10, 10: 11, 11: 9, 0: 1}

for i in mix_table:
    check_matrix[mix_table[i]] = original_matrix[i]
    # check_matrix[i] = original_matrix[mix_table[i]]

print check_matrix

charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
out = ""

for i in check_matrix:
    out += charset[(i - 0x29a) % 0x25]

print out
