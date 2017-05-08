#!/usr/bin/env python
# -*- coding: utf-8 -*-

import facebook
import requests
import xlwt
import pandas
from tempfile import TemporaryFile

#Initialisierung der Facebook Graph API, Übergabe des Tokens und Bearbeitung der zurückgegebenen Daten
token = "Füge hier Deinen Access Token ein"
graph = facebook.GraphAPI(access_token=token, version ="2.7")

#Zeitraum der Untersuchung festlegen. Durch die Begrenzung der API sind maximal 2 Jahre in die Vergangenheit möglich. 
zeitraum = []
for datum in pandas.date_range("2015-05-01", "2017-05-01", freq = "MS"):
	zeitraum.append(datum) 
	
#Liste der zu untersuchenden Vereine. Hier müssen die genauen Namen oder IDs der Facebook-Seiten angegeben werden.
Vereinsliste = ["meinSCP","SCFreiburg","VfB","Hannover96","DieSchanzer","SVDarmstadt1898eV","rbleipzig","KarlsruherSC","1.FCNuernberg","HSV","BVB","borussia.mg","herthabsc","bayer04fussball","vflwolfsburgfussball","FCBayern"]

for Verein in Vereinsliste:
	
	#Gewinnt die Daten für den oben definierten Zeitraum und die oben definierten Facebook-Seiten.
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


