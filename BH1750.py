#!/usr/bin/python

import time
import I2C


i2c = I2C.i2cMaster()
i2c.init(100,17,27) #i2c speed  = 100kbit/s SDA = GPIO17 SCL = GPIO27

def WriteByteData(addr,cmd):
    i2c.Start()
    i2c.WriteByte(addr)
    i2c.WriteByte(cmd)
    i2c.Stop()

def ReadWord(addr):
    i2c.Start()
    i2c.WriteByte(addr)
    high = i2c.ReadAck()
    low = i2c.ReadNack()
    i2c.Stop()
    val = (high << 8)+ low
    return val

def RawToLux(raw):
    return raw/1.2

def main():
    WriteByteData(0x46,0x10)
    time.sleep(0.024)
    print RawToLux(ReadWord(0x47))


if __name__ == "__main__":
    main()
