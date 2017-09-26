#!/usr/bin/env python

#Author Kaname Aimu
#Date 01-17-2017

import time
import os
from pyA20 import i2c

#Initialize module to use /dev/i2c-0
# i2c-0 is is the upper i2c port on your orangepi GPIO ports
#Physical:
# 3 - SDA.0
# 5 - SCL.0

i2c.init("/dev/i2c-0")

#the address of PCF8574
i2c.open(0x27)  

#i2c 1602 module pin defination
#LEDK is the K pin for LCD background light LED
#PCF8574 LCD1602
#D0      RS
#D1      RW
#D2      E
#D3      LEDK
#D4      D4
#D5      D5
#D6      D6
#D7      D7

C_LED=0x08*1

C_WC=0b00000000
C_WD=0b00000001

C_EN=0b00000100

def SetLed():
    i2c.write([C_LED])
    time.sleep(0.000001)

def LedOn():
    C_LED=0
    SetLed()

def LedOff():
    C_LED=0x08
    SetLed()

def Write4Bit(data):
    data=data<<4
    i2c.write([C_LED|data])
    time.sleep(0.00001)
    i2c.write([C_LED|C_WC|C_EN|data])
    time.sleep(0.000001)
    i2c.write([C_LED|C_WC|data])
    time.sleep(0.0001)

def WriteCommand(command):
    tmp=command&0xf0
    i2c.write([C_LED|tmp])
    time.sleep(0.00001)
    i2c.write([C_LED|C_WC|C_EN|tmp])
    time.sleep(0.0000001)
    i2c.write([C_LED|C_WC|tmp])
    time.sleep(0.00001)

    tmp=(command&0x0f)<<4
    i2c.write([C_LED|tmp])
    time.sleep(0.00001)
    i2c.write([C_LED|C_WC|C_EN|tmp])
    time.sleep(0.0000001)
    i2c.write([C_LED|C_WC|tmp])
    time.sleep(0.00001)

def WriteData(data):
    tmp=data&0xf0
    i2c.write([C_LED|tmp])
    time.sleep(0.00001)
    i2c.write([C_LED|C_WD|C_EN|tmp])
    time.sleep(0.0000001)
    i2c.write([C_LED|C_WD|tmp])
    time.sleep(0.00001)

    tmp=(data&0x0f)<<4
    i2c.write([C_LED|tmp])
    time.sleep(0.00001)
    i2c.write([C_LED|C_WD|C_EN|tmp])
    time.sleep(0.0000001)
    i2c.write([C_LED|C_WD|tmp])
    time.sleep(0.00001)

def WriteString(string):
    sl=list(string)
    for c in sl:
        WriteData(ord(c))

def InitLcd():
    SetLed()

    #Init the HD44780 using method from datasheet
    #SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
    Write4Bit(0x3)
    time.sleep(0.0045)
    
    Write4Bit(0x3)
    time.sleep(0.0045)
    
    Write4Bit(0x3)
    time.sleep(0.0045)
    
    Write4Bit(0x2)
    time.sleep(0.15)

    #Set proper working mode

    # 001 DL  N   F   - -
    # DL = 1 : 8 bits, DL = 0 : 4 bits
    # N  = 1 : 2 lines, N = 0 : 1 line
    # F  = 1 : 5x10 dots, F = 0 : 5x8 dots
    WriteCommand(0x28)

    # 000 1 S/C R/L   - -
    # S/C = 1 : display shift
    # S/C = 0 : cursor shift
    # R/L = 1 : shift to the right
    # R/L = 0 : shift to the left
    WriteCommand(0b00011000)

    # 000 0   1   D   C B
    # D - display on/off
    # C - cursor on/off
    # B - cursor blink on/off
    WriteCommand(0b00001110)

    # 000 0   0   1 I/D S
    # I/D = 1 : Increment
    # I/D = 0 : Decrement
    # S   = 1 : Accompanies display shift
    WriteCommand(0b00000110)    

    #Clear display
    WriteCommand(0x01)
    time.sleep(0.05)

def Setup():
    InitLcd()
    
    WriteCommand(0x80)
    WriteString('CPU temperature:')
    

def Loop():
    WriteCommand(0xC0)
    output=os.popen('cat /sys/devices/virtual/hwmon/hwmon1/temp1_input')
    temp=(output.read()).replace('\n','')
    WriteString(temp)
    
    time.sleep(1)

Setup()
while True:
    Loop()
    
i2c.close()

