import urllib2
import json
import psycopg2
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from pw import dbpass


# ident is the first item in the AED dataset 
ident = 1
#a variable representing the url pointing to the datast
aedObj = 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Health_WebMercator/MapServer/9/'+str(ident)+'?f=pjson'
aed = json.load(urllib2.urlopen(aedObj))
colm ={}

#tries to create the connection to the database, and prints failure message if necessarry
try:
    conn = psycopg2.connect(database='AED', user='postgres', password=dbpass, host='127.0.0.1', port='5432')
    
except:
    print "Database connection failed."
    
#a cursor used to perform queries
cur = conn.cursor()

#just here for development purposes. To be removed later
# try:
#     cur.execute("DROP TABLE IF EXISTS DEFIBS")
#     conn.commit()
# except:
# 	pass


while ident != 0:
	aedObj = 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Health_WebMercator/MapServer/9/'+str(ident)+'?f=pjson'
	aed = json.load(urllib2.urlopen(aedObj))

	try:
		colm['ident'] = aed['feature']['attributes']['OBJECTID']
		colm['acquired'] = aed['feature']['attributes']['DATE']
		colm['facility'] = aed['feature']['attributes']['FACILITY_NAME']
		colm['location'] = aed['feature']['attributes']['LOCATION']
		colm['x_coord'] = aed['feature']['attributes']['XCOORD']
		colm['y_coord'] = aed['feature']['attributes']['YCOORD']
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
		# cur. execute("""CREATE TABLE IF NOT EXISTS DEFIBS(ident INTEGER PRIMARY KEY NOT NULL,  acquired BIGINT, facility TEXT NOT NULL, location TEXT, brand TEXT, aed_model TEXT, aed_model_num TEXT, x_coord NUMERIC, y_coord NUMERIC, expires TEXT, replaced TEXT);""")
		# conn.commit()

		cur.execute("INSERT INTO DEFIBS(ident, acquired, facility, location, brand, aed_model, aed_model_num, x_cord, y_cord, expires, replaced)\
				VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (colm['ident'] , colm['acquired'], colm['facility'], colm['location'], colm['brand'], colm['model'], colm['model_num'], colm['x_coord'], colm['y_coord'], colm['expires'], colm['replaced']))
		conn.commit()

	except Exception as E:
		print str(E)
		pass