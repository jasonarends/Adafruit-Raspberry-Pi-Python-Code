#!/usr/bin/python

from Adafruit_7Segment import SevenSegment
segment = SevenSegment(address=(0x70))

segment.writeDigitRaw(0,109)
segment.writeDigitRaw(1,22)
segment.writeDigitRaw(2,0)
segment.writeDigitRaw(3,119)
segment.writeDigitRaw(4,109)

