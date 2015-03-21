#!/usr/bin/python

import sys
import time
from Adafruit_7Segment import SevenSegment
#from Adafruit_LEDBackpack import LEDBackpack

segment = SevenSegment(address=(0x70))
#lowlevel = LEDBackpack()

for i in range(0,128):
  segment.writeDigitRaw(0,i)
  time.sleep(0.05)

