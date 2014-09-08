#!/usr/bin/python

import sys
from lxml import etree
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import commands

COORD_DELTA_THRESHOLD = 0.005

with open(sys.argv[1]) as xmlfile:
	tree = etree.parse(xmlfile)
	root = tree.getroot()
	tracks = root.findall('{http://www.topografix.com/GPX/1/1}trk')
	lasttime = None
	for track in tracks:
		for trkseg in track.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
			for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
				if not 'lon' in trkpt.attrib or not 'lat' in trkpt.attrib:
					print trkpt.sourceline, 'has no lon or lat'
				else:
					try:
						lon = float(trkpt.attrib['lon'])
						lat = float(trkpt.attrib['lat'])
						try:
							prevlon
						except NameError:
							prevlon = lon
						try: 
							prevlat
						except NameError:
							prevlat = lat
						if abs(lon - prevlon) > COORD_DELTA_THRESHOLD or abs(lat - prevlat) > COORD_DELTA_THRESHOLD:
							print trkpt.sourceline, 'has a suspicious lon or lat'
					except ValueError:
						print trkpt.sourceline, 'has unparseable lon or lat'
				trkpttime = trkpt.find('{http://www.topografix.com/GPX/1/1}time')
				if trkpttime is None:
					print trkpt.sourceline, 'has no time'
				else:
					try:
						newtime = parse(trkpttime.text)
						if lasttime is None: 
							lasttime = newtime
						if relativedelta(newtime, lasttime).hours > 1:
							print lasttimesourceline, 'has a suspicious timestamp'
						lasttime = newtime
						lasttimesourceline = trkpttime.sourceline
					except:
						print trkpt.sourceline, 'has an unparseable time'
				prevlon = lon
				prevlat = lat