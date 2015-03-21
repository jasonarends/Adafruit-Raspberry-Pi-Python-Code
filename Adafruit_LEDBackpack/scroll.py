#!/usr/bin/python

def scroller(inputstr,pausetime=0.2,scrolloff=True):
    import time
    import datetime
    import sevensegdict
    from collections import deque
    from Adafruit_7Segment import SevenSegment
    from Adafruit_LEDBackpack import LEDBackpack
    
    segment = SevenSegment(address=0x70)
    ledbp = LEDBackpack()

    now = datetime.datetime.now()

    charqueue = deque(sevensegdict.str_to_seg(inputstr))
    if scrolloff: 
        charqueue.extend([0,0,0,0])
        
    #start with clear display
    word = deque([0,0,0,0])
    segment.writeDigitRaw(0,word[0])
    segment.writeDigitRaw(1,word[1])
    segment.writeDigitRaw(2,0)
    segment.writeDigitRaw(3,word[2])
    segment.writeDigitRaw(4,word[3])

    # Continually update the time on a 4 char, 7-segment display
    while(len(charqueue)):
        # get dimmer at night, brighter during day
        if now.hour > 22:
            ledbp.setBrightness(2)
        elif now.hour > 21:
            ledbp.setBrightness(8)
        elif now.hour > 7:
            ledbp.setBrightness(16)
        else:
            ledbp.setBrightness(2)
            
        word.popleft()
        word.append(charqueue.popleft())

        segment.writeDigitRaw(0,word[0])
        segment.writeDigitRaw(1,word[1])
        segment.writeDigitRaw(3,word[2])
        segment.writeDigitRaw(4,word[3])

        # Wait one second
        time.sleep(pausetime)

if __name__ == "__main__":
    import sys
    import argparse
      
    parser = argparse.ArgumentParser(description='Display a scrolling message on the attached 4 digit 7 segment LED display.')
    parser.add_argument('msg', default=sys.stdin, help='message to scroll')
    parser.add_argument('-p', '--pause', type=float, default=0.2, help='number of seconds to pause between chars')
    parser.add_argument('-s', '--scrolloff', action='store_false',  help='whether or not to scroll the message off the left side')
    args = parser.parse_args()
   
    scroller(args.msg, args.pause, args.scrolloff)
    