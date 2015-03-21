#!/usr/bin/python

from Adafruit_7Segment import SevenSegment
segment = SevenSegment(address=(0x70))

segment.writeDigitRaw(0,118)
segment.writeDigitRaw(1,92)
segment.writeDigitRaw(2,0)
segment.writeDigitRaw(3,54)
segment.writeDigitRaw(4,110)

