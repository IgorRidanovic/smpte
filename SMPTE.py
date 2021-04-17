#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Converts frames to SMPTE timecode of arbitrary frame rate and back.
# Copyright 2021, Igor Riđanović, Igor@hdhead.com, Meta Fide

class SMPTE(object):
	'''Frames to SMPTE timecode converter and reverse.'''

	def __init__(self):
		self.fps = 24
		self.df  = False


	def getframes(self, tc):
		'''Converts SMPTE timecode to frame count.'''

		if int(tc[9:]) > self.fps:
			raise ValueError ('SMPTE timecode to frame rate mismatch.', tc, self.fps)

		hours   = int(tc[:2])
		minutes = int(tc[3:5])
		seconds = int(tc[6:8])
		frames  = int(tc[9:])

		totalMinutes = int(60 * hours + minutes)

		# Drop frame calculation using the Duncan/Heidelberger method.
		if self.df:

			dropFrames = int(round(self.fps * 0.066666))
			timeBase   = int(round(self.fps))

			hourFrames   = int(timeBase * 60 * 60)
			minuteFrames = int(timeBase * 60)

			frm = int(((hourFrames * hours) + (minuteFrames * minutes) + (timeBase * seconds) + frames) - (dropFrames * (totalMinutes - (totalMinutes // 10))))

		# Non drop frame calculation.
		else:

			self.fps = int(round(self.fps))
			frm = int((totalMinutes * 60 + seconds) * self.fps + frames)

		return frm


	def gettc(self, frames):
		'''Converts frame count to SMPTE timecode.'''

		frames = abs(frames)

		# Drop frame calculation using the Duncan/Heidelberger method.
		if self.df:

			spacer = ':'
			spacer2 = ';'

			dropFrames         = int(round(self.fps * .066666))
			framesPerHour      = int(round(self.fps * 3600))
			framesPer24Hours   = framesPerHour * 24
			framesPer10Minutes = int(round(self.fps * 600))
			framesPerMinute    = int(round(self.fps) * 60 - dropFrames)

			frames = frames % framesPer24Hours

			d = frames // framesPer10Minutes
			m = frames % framesPer10Minutes


			if m > dropFrames:
				frames = frames + (dropFrames * 9 * d) + dropFrames * ((m - dropFrames) // framesPerMinute)

			else:
				frames = frames + dropFrames * 9 * d


			frRound = int(round(self.fps))
			hr = int(frames // frRound // 60 // 60)
			mn = int((frames // frRound // 60) % 60)
			sc = int((frames // frRound) % 60)
			fr = int(frames % frRound)

		# Non drop frame calculation.
		else:

			self.fps = int(round(self.fps))
			spacer  = ':'
			spacer2 = spacer

			frHour = self.fps * 3600
			frMin  = self.fps * 60

			hr = int(frames // frHour)
			mn = int((frames - hr * frHour) // frMin)
			sc = int((frames - hr * frHour - mn * frMin) // self.fps)
			fr = int(round(frames -  hr * frHour - mn * frMin - sc * self.fps))



		# Return SMPTE timecode string.
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
