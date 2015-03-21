#!/usr/bin/python

import collections

def str_to_seg(s = '    '):
	"""Return decimals for raw digit writing to 7 segment display
	based on ascii input."""

	# define how to display each possible letter.
	# special cases where 2 letters can be displayed in one 7seg
	# | = ll
	# m = il
	# k = li
	# I is on left, l is on right
	# i is on left, ! is on right

	d = collections.defaultdict(lambda: 0)

	d.update({\
	'A': 119,\
	'b': 124,\
	'C': 57, \
	'c': 88, \
	'd': 94, \
	'E': 121,\
    'e': 121,\
	'F': 113,\
    'f': 113,\
	'G': 61, \
	'g': 111,\
	'H': 118,\
	'h': 116,\
	'I': 48, \
	'i': 16, \
	'!': 4,  \
	'J': 30, \
	'j': 14, \
	'k': 52, \
	'L': 56, \
	'l': 6,  \
	'|': 54, \
	'm': 22, \
	'n': 84, \
	'O': 63, \
	'o': 92, \
	'p': 115,\
	'q': 103,\
	'r': 80, \
	'S': 109,\
    's': 109,\
	't': 120,\
	'U': 62, \
	'u': 28, \
	'y': 110,\
	'z': 91, \
	'=': 72, \
	'_': 8,  \
	'-': 64, \
	'0': 63, \
	'1': 6,  \
	'2': 91, \
	'3': 79, \
	'4': 102,\
	'5': 109,\
	'6': 125,\
	'7': 7,  \
	'8': 127,\
	'9': 111})

	n = []

	for i in range(len(s)):
		n.append(d[s[i]])

	return n

