import urllib2
import json
import psycopg2
from time import strftime
from datetime import datetime
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from pw import dbpass


# ident is the first item in the AED dataset 
ident = 1
#a variable representing the url pointing to the dataset, beginning with the first item
aedObj = 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Health_WebMercator/MapServer/9/'+str(ident)+'?f=pjson'
aed = json.load(urllib2.urlopen(aedObj))

#an empty dictionary to hold the table data
colm ={}

#tries to create the connection to the database, and prints failure message if necessarry
try:
    conn = psycopg2.connect(database='AED', user='postgres', password=dbpass, host='127.0.0.1', port='5432')
    
except:
    print "Database connection failed."
    
#a cursor used to perform queries
cur = conn.cursor()

#just here for development purposes. To be removed later
try:
    cur.execute("DROP TABLE IF EXISTS DEFIBS")
    conn.commit()
except:
	pass


while ident != 0: #consider making this none/null instead of zero
	aedObj = 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Health_WebMercator/MapServer/9/'+str(ident)+'?f=pjson'
	aed = json.load(urllib2.urlopen(aedObj))

	try:
		colm['ident'] = aed['feature']['attributes']['OBJECTID']
		
		# checks if the item in the date field contains all numbers
		if str(aed['feature']['attributes']['DATE']).isdigit() == True:
			
			#slices the string  of the date field to remove the trailing zeros and assigned it to timestamp
			timestamp = str(aed['feature']['attributes']['DATE'])[0:-3]
			
			#converts timestamp into month-day-year format to be inserted into the table
			converted = datetime.fromtimestamp(int(timestamp)).strftime('%m-%d-%Y')
			colm['acquired'] = converted
		else:
			colm['acquired'] = aed['feature']['attributes']['DATE']

		colm['facility'] = aed['feature']['attributes']['FACILITY_NAME']
		colm['location'] = aed['feature']['attributes']['LOCATION']
		colm['Lng'] = aed['feature']['geometry']['x']
		colm['Lat'] = aed['feature']['geometry']['y']
		colm['expires'] = aed['feature']['attributes']['PADS_EXPIRATION_DATE']
		colm['replaced'] = aed['feature']['attributes']['REPLACED']
		colm['brand'] = aed['feature']['attributes']['AED_BRAND_MANUFACTURER']
		colm['model'] = aed['feature']['attributes']['AED_BRAND_TEXT']
		colm['model_num'] = aed['feature']['attributes']['MODEL_NUMBER']

		ident = ident + 1
		
	except Exception as E:
		print str(E)
		ident = 0
		pass


	try:
		cur. execute("""CREATE TABLE IF NOT EXISTS DEFIBS(ident INTEGER PRIMARY KEY NOT NULL,  acquired DATE, facility TEXT NOT NULL, location TEXT, brand TEXT, aed_model TEXT, aed_model_num TEXT, Lng DOUBLE PRECISION, Lat DOUBLE PRECISION, expires TEXT, replaced TEXT);""")
		conn.commit()

		cur.execute("INSERT INTO DEFIBS(ident, acquired, facility, location, brand, aed_model, aed_model_num, Lng, Lat, expires, replaced)\
				VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (colm['ident'] , colm['acquired'], colm['facility'], colm['location'], colm['brand'], colm['model'], colm['model_num'], colm['Lng'], colm['Lat'], colm['expires'], colm['replaced']))
		conn.commit()

	except Exception as E:
		print str(E)
		pass