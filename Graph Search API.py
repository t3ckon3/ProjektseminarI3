#!/usr/bin/env python
# -*- coding: utf-8 -*-

import facebook
import requests
import xlwt
import pandas
from tempfile import TemporaryFile

#Initialisierung der Facebook Graph API, Übergabe des Tokens und Bearbeitung der zurückgegebenen Daten
token = "EAADLS5p1ZA7ABALEZA1FoiMYsKN8FLy3ZApwutavrCVRvpjiKYayOwhAYmenGBVy1vn8Aw8fGCSA0UMzCZBllK0FmrVYO4EQbR3yR4kK1rcJiHduHVk18IfOPoZAM8f5fXv2Jq0lYEEoZCexbwVqiK0KmvM9Fd0fwZD"
graph = facebook.GraphAPI(access_token=token, version ="2.7")

#Zeitraum der Untersuchung festlegen. Das Maximum sind zwei Jahre in die Vergangenheit.
zeitraum = []
for datum in pandas.date_range("2015-05-01", "2017-05-01", freq = "MS"):
	zeitraum.append(datum) 
	
#Liste der zu untersuchenden Vereine, der Name der Facebookseite wie er in der URL zu finden ist ist anzugeben
Vereinsliste = ["meinSCP","SCFreiburg","VfB","Hannover96","DieSchanzer","SVDarmstadt1898eV","rbleipzig","KarlsruherSC","1.FCNuernberg","HSV","BVB","borussia.mg","herthabsc","bayer04fussball","vflwolfsburgfussball","FCBayern"]

for Verein in Vereinsliste:
	
	#Gewinnt die Daten für den oben definierten Zeitraum und die oben definierten Facebookseiten.
	daten = []
	for i, timestamp in enumerate(zeitraum):
		if timestamp == zeitraum[len(zeitraum)-1]:
			break
		pagelikes = graph.request("/%s/insights/page_fans_country/lifetime?&since=%s&until=%s" % (Verein,timestamp,zeitraum[i+1])) 
		daten.append(pagelikes["data"][0]["values"])
	
	#Filterung nach Ergebnissen der Deutschen Nutzer
	germany = []
	for j in range (0,len(daten)):
		for i in range(0,len(daten[j])):
			germany.append(daten[j][i]["value"]["DE"])
		
	#Schreibt die Daten in ein Excelsheet zur weiteren Verarbeitung	
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet(Verein)
	dates = []

	for date in pandas.date_range("2015-05-01", "2017-04-30"):
		dates.append(date)

	for j,e in enumerate(germany):
		Sheet.write(j,0,e)
		Sheet.write(j,1,dates[j])

	Exceldatei.save("%s.xls" %Verein)
	Exceldatei.save(TemporaryFile())
	print "Done with %s" %Verein


