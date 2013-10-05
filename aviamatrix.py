#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib,urllib2,re,json

class Unbuffered:
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout=Unbuffered(sys.stdout)

def getPrices(flights):
	priceo = None
	pricel = re.search('<price>(\d+)</price>',flights).group(1)
	while flights.find('<variant>')>=0:
		variant = flights[flights.find('<variant>'):flights.find('</variant>')]
		flights = flights[flights.find('</variant>')+9:]
		tempra = re.search('<price>(\d+)</price>',variant).group(1)

		clean = 1
		while variant.find('<flight>')>0:
			variant = variant[variant.find('</flight>')+8:]
			if -1< variant.find('<flight>')<8 : clean=0
		if clean:
			priceo = tempra
			break

	return (pricel, priceo)
	
from datetime import date,timedelta

y = 2013
frd,frm,tod,tom = 30,4, 7,5
where = "NCE"
where = raw_input('Destination: ')
frm = int(raw_input('From, month:'))
frd = int(raw_input('From, day:'))
tom = int(raw_input('To, month:'))
tod = int(raw_input('To,day:'))

wd = ['пн','вт','ср','чт','пт','сб','вс']

fromdate = date(y,frm,frd)
todate = date(y,tom,tod)
nextday = fromdate+timedelta(1)

print "Обратно:\t",
for todelta in range(-3,3):
	print wd[(todate+timedelta(todelta)).weekday()],todate+timedelta(todelta),'\t',

for fromdelta in range (-3,3):
	print " " 
	currfrom = fromdate+timedelta(fromdelta)
	print wd[currfrom.weekday()], currfrom, '\t',
 	for todelta in range(-3,3):
 		
 		currto = todate+timedelta(todelta)
 	
		try:
			flights = urllib2.urlopen('http://api.eviterra.com/avia/v1/variants.xml?from=MOW&to=%s&date1=2013-%d-%d&date2=2013-%d-%d'%(where,currfrom.month,currfrom.day,currto.month,currto.day)).read()
		except  urllib2.HTTPError as e: 
			print 'Error connecting to Eviterra: ',e.read()
			
		try:
			(pricel, priceo) = getPrices(flights)
			print pricel,priceo,'\t',
		except: 
			print ' - - \t',

print ""