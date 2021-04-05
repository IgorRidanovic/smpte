# SMPTE Timecode Arithmetic Class for Python 2.7 and 3.x

## Usage Examples

```
s = SMPTE()

&#35; Convert 24 timecode string to frame count (24 is set by default)
tcString = '01:00:00:00'
print(s.getframes(tcString))

&#35; Convert frame count to 29.97 drop frame timecode string
s.fps = 29.97
s.df = True
frameCount = 1800
print(s.gettc(frameCount))
```

## Frame Rates and Drop Frame

All fractional frame rates are rounded up to the nearest integer since all calculations must use integers. There is no need to specify 23.976 when calculating 23.976 timecode since this is covered by the default 24 value.

In fact, the s.fps = 29.97 in the above example will get rounded to 30, but we use 29.97 in the example for historical consistency and clarity--there is no such thing as 30 fps DF TC.

Remember that all timecode except DF is real time clock inaccurate.

The gettc() uses Andrew Duncan method of calculating the SMPTE timecode string. See his excellent article at http://www.andrewduncan.net/timecodes/.
