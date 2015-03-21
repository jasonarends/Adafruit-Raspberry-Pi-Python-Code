#!/usr/bin/python

import time, datetime, scroll, os
from Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack import LEDBackpack


segment = SevenSegment(address=0x70)
ledbp = LEDBackpack()

pid = os.getpid()
with open('/home/pi/.thermclock.pid','w') as p:
    p.write(str(pid))

def getweather(dtnow=datetime.datetime.now()):
    # get conditions last reported (cron job updates this)
    returnlist = []
    with open('/home/pi/x10/current.txt') as f:
        for line in f:
            if 'Temperature:' in line:
                sa = line.split()
                returnlist.append("out =   " + sa[1].split('.')[0] + sa[2])
            elif 'Windchill:' in line:
                sb = line.split()
                returnlist.append("chi| =   " + sb[1].split('.')[0] + sb[2])
                
    with open('/home/pi/x10/suninfo.txt') as s:
        for line in s:
            if 'Sun rises' in line:
                sc = line.split()
                sunrisestr = sc[2]
                sunsetstr = sc[5]
                break
                
    sunrisetime = dtnow.replace(hour=int(sunrisestr[:2]), minute=int(sunrisestr[2:]))
    sunsettime = dtnow.replace(hour=int(sunsetstr[:2]), minute=int(sunsetstr[2:]))
    if dtnow < sunrisetime:
        returnlist.append("Sun uP =  " + str(sunrisetime.hour) + sunrisestr[2:])
    elif dtnow < sunsettime:
        returnlist.append("Sun dn =  " + str(int(sunsettime.hour)%12) + sunsetstr[2:])
    
    return returnlist
    
weatherlist = getweather()
currentweatheritem = 0

# Continually update the time on a 4 char, 7-segment display
while(True):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    # try to update weather a few times (cron updates at 10 past)
    if (minute == (11 or 41)) and (second == (15 or 46)):
        weatherlist = getweather(now)

    # get dimmer at night, brighter during day
    if hour > 22:
        ledbp.setBrightness(2)
    elif hour > 21:
        ledbp.setBrightness(8)
    elif hour > 7:
        ledbp.setBrightness(16)
    else:
        ledbp.setBrightness(2)

    # set left top dot to indicate pm and undo 24-hr time
    # colon is 2 and dot is 4
    if hour > 12:
        hour = hour - 12
        colon_on = 6
        colon_off = 4
    else:
        colon_on = 2
        colon_off = 0

    #every 20 sec, scroll some weather
    if not second % 20:
        #print 'weatherlist contains:',len(weatherlist)
        #print 'current index:',currentweatheritem
        # determine how big weatherlist is and iterate through them
        if currentweatheritem < len(weatherlist):
            #print 'weather item contains:',weatherlist[currentweatheritem]
            scroll.scroller(weatherlist[currentweatheritem],0.1,False)
            time.sleep(2)
            currentweatheritem += 1
        else:
            #print 'exceeded top, reset to 0.  item contains:',weatherlist[0]
            scroll.scroller(weatherlist[0],0.1,False)
            time.sleep(2)
            currentweatheritem = 1

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
