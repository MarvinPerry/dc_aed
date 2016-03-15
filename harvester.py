import urllib2
import json
import psycopg2
from time import strftime
from datetime import datetime
from flask import Flask, render_template, request
from pyproj import Proj, transform
from pw import *
import pdb

#### Begining trace here ####
# pdb.set_trace()


# defines the incoming coordinate system as 3857 and the system that he want as 4326 for conversion later
inCoordSys = Proj(init='epsg:3857')
outCoordSys = Proj(init='epsg:4326')


# ident is the first item in the AED dataset 
ident = 1

#a variable representing the url pointing to the dataset, beginning with the first item
aedObj = 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Health_WebMercator/MapServer/9/query?where=1%3D1&text=&objectIds='+str(ident)+'&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson'
aed = json.load(urllib2.urlopen(aedObj))

#empty dictionary to hold the table data
colm ={}

#tries to create the connection to the database, and prints failure message if necessarry
try:
    conn = psycopg2.connect(database=AED, user=postgres, password=dbpass, host=host, port=port)
    
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


while ident != 0: #couunter to keep track of the number of aeds
	aedObj = 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Health_WebMercator/MapServer/9/query?where=1%3D1&text=&objectIds='+str(ident)+'&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson'
	aed = json.load(urllib2.urlopen(aedObj))

	try:

		colm['ident'] = aed['features'][0]['attributes']['OBJECTID']
		
		# checks if the item in the date field contains all numbers
		if str(aed['features'][0]['attributes']['DATE']).isdigit() == True:
			
			#slices the string  of the date field to remove the trailing zeros and assigned it to timestamp
			timestamp = str(aed['features'][0]['attributes']['DATE'])[0:-3]
			
			#converts timestamp into month-day-year format to be inserted into the table
			converted = datetime.fromtimestamp(int(timestamp)).strftime('%m-%d-%Y')
			colm['acquired'] = converted
		else:
			colm['acquired'] = aed['features'][0]['attributes']['DATE']

		colm['facility'] = aed['features'][0]['attributes']['FACILITY_NAME']
		colm['location'] = aed['features'][0]['attributes']['LOCATION']
		
		# if there is location data in the X coordinate field, convert it to proper lat and lng
		if aed['features'][0]['geometry']['x']:
			try:
				#transform is a function in PyProj that accepts coordinates in one format and converts them to another format
				colm['Lng'],colm['Lat'] = transform (inCoordSys, outCoordSys, aed['features'][0]['geometry']['x'], aed['features'][0]['geometry']['y'])
				
				#this block of code reverse geocodes the lat and long coordinates and returns an address
				itemUrl = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(colm['Lat'])+','+str(colm['Lng'])+'&key='+googMapKey
				revGeo = json.load(urllib2.urlopen(itemUrl))
				addr = revGeo['results'][0]['formatted_address']
				
			except:
				colm['Lng'] = aed['feature']['geometry']['x']
				colm['Lat'] = aed['feature']['geometry']['y']

		colm['expires'] = aed['features'][0]['attributes']['PADS_EXPIRATION_DATE']
		colm['replaced'] = aed['features'][0]['attributes']['REPLACED']
		colm['brand'] = aed['features'][0]['attributes']['AED_BRAND_MANUFACTURER']
		colm['model'] = aed['features'][0]['attributes']['AED_BRAND_TEXT']
		colm['model_num'] = aed['features'][0]['attributes']['MODEL_NUMBER']
		colm['address'] = addr

		ident = ident + 1
		
	except Exception as E:
		print str(E)
		ident = 0
		pass


	try:
		cur. execute("CREATE TABLE IF NOT EXISTS DEFIBS(ident INTEGER PRIMARY KEY NOT NULL, acquired DATE, facility TEXT, location TEXT, brand TEXT, aed_model TEXT, aed_model_num TEXT, Lng FLOAT, Lat FLOAT, expires TEXT, replaced TEXT, address TEXT);")
		conn.commit()

		cur.execute("INSERT INTO DEFIBS(ident, acquired, facility, location, brand, aed_model, aed_model_num, Lng, Lat, expires, replaced, address)\
				VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (colm['ident'] , colm['acquired'], colm['facility'], colm['location'], colm['brand'], colm['model'], colm['model_num'], colm['Lng'], colm['Lat'], colm['expires'], colm['replaced'], colm['address']))
		conn.commit()

	except Exception as E:
		print str(E)
		pass





