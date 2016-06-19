#!/usr/bin/python

import time
import smbus

#Address of the BH1750
address = 0x23
bus = smbus.SMBus(1)

def read_byte(addr):
    return bus.read_byte_data(address,addr)

def read_word(addr):
    high = bus.read_byte_data(address,addr)
    low = bus.read_byte_data(address,addr+1)
    val = (high << 8)+ low
    return val


def main():
    #Wake up the BH170
    bus.write_byte(address,0x1)

    bus.write_byte(address,0x10)
    time.sleep(0.24)
    bus.read_byte(address,0x10)

if __name__ == "__main__":
    main()
