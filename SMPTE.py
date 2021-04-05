#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Converts frames to SMPTE timecode of arbitrary frame rate and back.
# Copyright 2018, Igor Riđanović, Igor@hdhead.com, Meta Fide

class SMPTE(object):
	'''Frames to SMPTE timecode converter and reverse.'''

	def __init__(self):
		self.fps = 24
		self.df  = False

	def getframes(self, tc):
		'''Converts SMPTE timecode to frame count.'''

		# Always round fractional frame rate.
		self.fps = int(round(self.fps))

		if int(tc[9:]) > self.fps:
			raise ValueError ('SMPTE timecode to frame rate mismatch.', tc, self.fps)

		# Calculate timecode to frames for fps time base
		min = int(tc[:2])*60 + int(tc[3:5])
		sec = int(tc[6:8])
		frm =	int((min*60 + sec) * self.fps + int(tc[9:]))

		# Drop frame adjustment
		if self.df:
			# Subtract 2 frames for each minute...
			dffrm =  frm - min * 2
			# ...except every 10 minutes.
			tens = min / 10
			dffrm += tens * 2
			return dffrm

		return frm


	def gettc(self, frames):
		'''Converts frame count to SMPTE timecode.'''

		frames = abs(frames)

		# Always round fractional frame rate.
		self.fps = int(round(self.fps))

		# SMPTE string spacer.
		spacer  = ':'

		# Drop frame calculation.
		if self.df:
			spacer2 = ';'

			# www.andrewduncan.net/timecodes/ special DF sauce.
			d = frames // 17982
			m = frames % 17982
			frames +=  18 * d + 2 * (m - 2) // 1798

			hr = int(frames // self.fps // 60 // 60 % 24)
			mn = int(frames // self.fps // 60 % 60)
			sc = int(frames // self.fps % 60)
			fr = int(frames %  self.fps)

		# Non drop frame calculation.
		else:
			spacer2 = spacer

			frHour = self.fps * 3600
			frMin  = self.fps * 60

			hr = int(frames // frHour)
			mn = int((frames - hr * frHour) // frMin)
			sc = int((frames - hr * frHour - mn * frMin) // self.fps)
			fr = int(round(frames -  hr * frHour - mn * frMin - sc * self.fps))

		return(
				str(hr).zfill(2) + spacer +
				str(mn).zfill(2) + spacer +
				str(sc).zfill(2) + spacer2 +
				str(fr).zfill(2)
				)

if __name__ == '__main__':

	# Drop frame example.
	s = SMPTE()
	s.fps = 29.97
	s.df = True

	print(s.gettc(1800))
