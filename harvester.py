import urllib2
import json
import psycopg2


# ident is the first item in the AED dataset 
ident = 1
#a variable representing the url pointing to the datast
aedObj = 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Health_WebMercator/MapServer/9/'+str(ident)+'?f=pjson'
aed = json.load(urllib2.urlopen(aedObj))
schema ={}

#tries to create the connection to the database, and prints failure message if necessarry
try:
    conn = psycopg2.connect(database='AED', user='postgres', password='*****', host='127.0.0.1', port='5432')
    
except:
    print "Database connection failed."
    
#a cursor used to perform queries
cur = conn.cursor()

#just here for development purposes. To be removed later
try:
    cur.execute("DROP TABLE IF EXISTS AED")
    conn.commit()
except:
	pass


while ident != 0:
	aedObj = 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Health_WebMercator/MapServer/9/'+str(ident)+'?f=pjson'
	aed = json.load(urllib2.urlopen(aedObj))

	try:
		schema['ident'] = aed['feature']['attributes']['OBJECTID']
		schema['acquired'] = aed['feature']['attributes']['DATE']
		schema['facility'] = aed['feature']['attributes']['FACILITY_NAME']
		schema['location'] = aed['feature']['attributes']['LOCATION']
		schema['x_coord'] = aed['feature']['attributes']['XCOORD']
		schema['y_coord'] = aed['feature']['attributes']['YCOORD']
		schema['expires'] = aed['feature']['attributes']['PADS_EXPIRATION_DATE']
		schema['replaced'] = aed['feature']['attributes']['REPLACED']
		schema['brand'] = aed['feature']['attributes']['AED_BRAND_MANUFACTURER']
		schema['model'] = aed['feature']['attributes']['AED_BRAND_TEXT']
		schema['model_num'] = aed['feature']['attributes']['MODEL_NUMBER']

		ident = ident + 1
		
	except Exception as E:
		print str(E)
		ident = 0
		pass


	try:
		cur. execute("""CREATE TABLE IF NOT EXISTS AED(id INTEGER PRIMARY KEY NOT NULL,  acquired BIGINT, facility TEXT NOT NULL, location TEXT, brand TEXT, model TEXT, model_num TEXT, x_coord DOUBLE PRECISION, y_coord DOUBLE PRECISION, expires DATE, replaced TEXT);""")
		conn.commit()

		cur.execute("INSERT INTO AED(id, acquired, facility, location, brand, model, model_num, x_coord, y_coord, expires, replaced)\
				VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (schema['ident'] , schema['acquired'], schema['facility'], schema['location'], schema['brand'], schema['model'], schema['model_num'], schema['x_coord'], schema['y_coord'], schema['expires'], schema['replaced']))
		conn.commit()

	except Exception as E:
		print str(E)
		pass