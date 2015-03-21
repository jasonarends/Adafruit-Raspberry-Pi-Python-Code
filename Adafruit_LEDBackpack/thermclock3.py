#!/usr/bin/python

import time, datetime, os
from Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack import LEDBackpack
from datetime import date, datetime


segment = SevenSegment(address=0x70)
ledbp = LEDBackpack()

# Continually update the time on a 4 char, 7-segment display
while(True):
    now = datetime.utcnow()
    hour = now.hour
    minute = now.minute
    second = now.second


    ledbp.setBrightness(8)

    # set left top dot to indicate pm and undo 24-hr time
    # colon is 2 and dot is 4
    colon_on = 2
    colon_off = 0

    # Set hours
    if hour > 9:
        segment.writeDigit(0, int(hour / 10))     # Tens
    else:
        segment.writeDigitRaw(0,0)
    segment.writeDigit(1, hour % 10)          # Ones
    # Set minutes
    segment.writeDigit(3, int(minute / 10))   # Tens
    segment.writeDigit(4, minute % 10)        # Ones

    #blink colon every sec
    if (second % 2):
        blink = colon_on
    else:
        blink = colon_off
    segment.writeDigitRaw(2,blink)

    # Wait one second
    time.sleep(1)
