#!/usr/bin/env python

#Converts frames to SMPTE timecode of arbitrary frame rate and back.
#For DF calculations use 29.976 frame rate.
#Igor Ridanovic, igor@HDhead.com

def validatetc(tc, fps):
	"""Validates SMPTE timecode"""
	if len(tc) != 11:
		raise ValueError ('Malformed SMPTE timecode', tc)
	if int(tc[9:]) > fps:
		raise ValueError ('SMPTE timecode to frame rate mismatch', tc, fps)

def fromtc(tc, fps):
	"""Converts SMPTE timecode to frame count."""
	validatetc(tc, fps)
	return	int(round((int(tc[:2])*3600 +
			int(tc[3:5])*60 +
			int(tc[6:8]))*fps +
			int(tc[9:])))

def totc(x, fps):
	"""Converts frame count to SMPTE timecode.""" 
	spacer = ':'
	frHour = fps * 3600
	frSec = fps * 60
	hr = int(x // frHour)
	mn = int((x - hr * frHour) // frSec)
	sc = int((x - hr * frHour - mn * frSec) // fps)
	fr = int(round(x -  hr * frHour - mn * frSec - sc * fps))
       
	return(
	str(hr).zfill(2) + spacer +
	str(mn).zfill(2) + spacer +
	str(sc).zfill(2) + spacer +
	str(fr).zfill(2))
