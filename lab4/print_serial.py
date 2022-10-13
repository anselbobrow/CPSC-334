#!/usr/bin/env python

# python -m pip install pyserial
import serial
from time import sleep 

# include a timeout if there are no \n chars in the serial output
esp = serial.Serial("/dev/cu.usbserial-210", 115200, timeout=0)

while True:
    print(esp.readline().decode("utf-8"), end="")
    # sleep(0.1) # no sleep needed if timeout=0
