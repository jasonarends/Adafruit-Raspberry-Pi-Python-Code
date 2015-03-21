#!/usr/bin/python

from Adafruit_7Segment import SevenSegment
segment = SevenSegment(address=(0x70))

segment.writeDigitRaw(0,14)
segment.writeDigitRaw(1,119)
segment.writeDigitRaw(2,0)
segment.writeDigitRaw(3,109)
segment.writeDigitRaw(4,121)

