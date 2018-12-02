#!/usr/bin/env python3



def bin_to_dec(binary):
    dec_number = 0
    posVal = 0
    for i in range(len(binary)-1, -1, -1):
        dec_number += int(binary[i])*(2**posVal)
        posVal += 1
    return dec_number

bin_str = "1001010"
print("Bin-to-decimal: " + bin_str + " = " + str(bin_to_dec(bin_str)))

