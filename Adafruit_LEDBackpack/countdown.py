#!/usr/bin/python

import time, datetime, sys, sevensegdict, argparse, os, scroll
from Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack import LEDBackpack

parser = argparse.ArgumentParser(description='Display a countdown on the attached 4 digit 7 segment LED display.')
parser.add_argument('mins', type=int, help='number of integer mins to count down')
parser.add_argument('-w', '--word', default='    ', help='word to display at end of countdown (4 characters)')
args = parser.parse_args()

inputmins = args.mins
inputword = args.word

with open('/home/pi/.thermclock.pid') as p:
    pid = int(p.read())

os.kill(pid,19)
	
segment = SevenSegment(address=0x70)
ledbp = LEDBackpack()

duration = datetime.timedelta(minutes=inputmins)
starttime = datetime.datetime.now()
stoptime = starttime + duration
now = starttime

# Continually update the time on a 4 char, 7-segment display
while(stoptime>now):
    now = datetime.datetime.now()
    # get dimmer at night, brighter during day
    if now.hour > 22:
        ledbp.setBrightness(2)
    elif now.hour > 21:
        ledbp.setBrightness(8)
    elif now.hour > 7:
        ledbp.setBrightness(16)
    else:
        ledbp.setBrightness(2)

    timeleft = stoptime - now
    secondsleft = int(timeleft.total_seconds())
    minute = int(secondsleft/60)
    second = secondsleft - minute*60
    
    # Set mins
    if minute == 0:
        segment.writeDigitRaw(0,0)
        segment.writeDigitRaw(1,0)
    elif minute < 10:
        segment.writeDigitRaw(0,0)
        segment.writeDigit(1, minute % 10)
    else:
        segment.writeDigit(0, int(minute / 10))     # Tens
        segment.writeDigit(1, minute % 10)          # Ones
        
    # Set seconds
    if minute == 0:
        if second < 10:
            segment.writeDigitRaw(3,0)
            segment.writeDigit(4, second)
        else:
            segment.writeDigit(3, int(second / 10))
            segment.writeDigit(4, second % 10)
    else:
        segment.writeDigit(3, int(second / 10))   # Tens
        segment.writeDigit(4, second % 10)        # Ones
        
    # Toggle colon
    if (second % 2):
        blink = 2
    else:
        blink = 0

    segment.writeDigitRaw(2,blink)
    # Wait one second
    time.sleep(1)

segment.writeDigitRaw(4,0)

scroll.scroller(inputword,0.1,False)

ledbp.setBlinkRate(1)

time.sleep(60)

ledbp.setBlinkRate(0)

# clear display
segment.writeDigitRaw(0,0)
segment.writeDigitRaw(1,0)
segment.writeDigitRaw(3,0)
segment.writeDigitRaw(4,0)

os.kill(pid,18)