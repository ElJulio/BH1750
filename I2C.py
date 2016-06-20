#!/usr/bin/python

#Soft implementation of an i2c Master
#Author:

import time
import RPi.GPIO as GPIO

class i2cMaster:

    int_clk = -1

    SDA = 17 #default sda
    SCL = 27 #default scl

    def tick(self,anz):
        time.sleep(anz*self.int_clk)

    def init(self,bitrate,SDAPIN,SCLPIN):
        if(SDAPIN != SCLPIN):
            self.SCL = SCLPIN
            self.SDA = SDAPIN

        else:
            print "SDA = GPIO"+str(self.SDA)+"  SCL = GPIO"+str(self.SCL)

        #configer SCL as output
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.SCL, GPIO.OUT)
        GPIO.setup(self.SDA, GPIO.OUT)
        GPIO.output(self.SDA, GPIO.HIGH)
        GPIO.output(self.SCL, GPIO.HIGH)


        if bitrate == 100:
            self.int_clk = 0.0000025
        elif bitrate == 400:
            self.int_clk = 0.000000625
        elif bitrate == 1000:
            self.int_clk = 1
        elif bitrate == 3200:
            self.int_clk = 1

    def Start(self):
        #SCL
        #  ______
        #  |     |______
        #SDA
        #  ___
        #  |  |_________

        GPIO.setup(self.SDA, GPIO.OUT) #cnfigure SDA as output

        GPIO.output(self.SDA, GPIO.HIGH)
        GPIO.output(self.SCL, GPIO.HIGH)
        self.tick(1)
        GPIO.output(self.SDA, GPIO.LOW)
        self.tick(1)
        GPIO.output(self.SCL, GPIO.LOW)
        self.tick(2)


    def ReadAck(self):
        GPIO.setup(self.SDA, GPIO.IN)
        readbuffer =0
        for i in range(8):
            GPIO.output(self.SCL, GPIO.HIGH)
            self.tick(2)
            readbuffer |= (GPIO.input(self.SDA)<< 7) >> i
            GPIO.output(self.SCL, GPIO.LOW)
            self.tick(2)

        GPIO.setup(self.SDA, GPIO.OUT)
        GPIO.output(self.SDA, GPIO.LOW)
        GPIO.output(self.SCL, GPIO.HIGH)
        self.tick(2)
        GPIO.output(self.SCL, GPIO.LOW)
        GPIO.output(self.SDA, GPIO.LOW)
        self.tick(2)
        return readbuffer

    def ReadNack(self):
        GPIO.setup(self.SDA, GPIO.IN)
        readbuffer =0
        for i in range(8):
            GPIO.output(self.SCL, GPIO.HIGH)
            self.tick(2)
            readbuffer |= (GPIO.input(self.SDA)<< 7) >> i
            GPIO.output(self.SCL, GPIO.LOW)
            self.tick(2)

        GPIO.setup(self.SDA, GPIO.OUT)
        GPIO.output(self.SDA, GPIO.HIGH)
        GPIO.output(self.SCL, GPIO.HIGH)
        self.tick(2)
        GPIO.output(self.SCL, GPIO.LOW)
        GPIO.output(self.SDA, GPIO.LOW)
        self.tick(2)
        return readbuffer

    def WriteByte(self,byte):
        if byte > 0xff:
            return -1
        #print byte
        GPIO.setup(self.SDA, GPIO.OUT)
        for i in range(8):
            #MSB First
            if (byte << i) & 0x80 == 0x80:
                GPIO.output(self.SDA, GPIO.HIGH)
                GPIO.output(self.SCL, GPIO.HIGH)
                self.tick(2)
                GPIO.output(self.SCL, GPIO.LOW)
                GPIO.output(self.SDA, GPIO.LOW)
                self.tick(2)
            else:
                GPIO.output(self.SDA, GPIO.LOW)
                GPIO.output(self.SCL, GPIO.HIGH)
                self.tick(2)
                GPIO.output(self.SCL, GPIO.LOW)
                self.tick(2)

        GPIO.setup(self.SDA, GPIO.IN)
        GPIO.output(self.SCL, GPIO.HIGH)
        #self.tick(1)
        #Get The ACK
        #if GPIO.input(self.SDA):
        #    print "ACK"
        #else:
        #    print "NACK"
        self.tick(2)
        GPIO.output(self.SCL, GPIO.LOW)
        self.tick(2)


    def Stop(self):
        #SCL
        #  _____________
        #  |
        #SDA
        #     __________
        #   __|
        GPIO.setup(self.SDA, GPIO.OUT) #cnfigure SDA as output

        GPIO.output(self.SDA, GPIO.LOW)
        GPIO.output(self.SCL, GPIO.HIGH)
        self.tick(1)
        GPIO.output(self.SDA, GPIO.HIGH)
        self.tick(3)
