# DC AED
This project is a tool for someone to find vital information about all the registered automatic external defibrillators in Washington D.C.

## Motivation
The DC AED project is an attempt to gain experience tying several core web development concepts together (API calls, Flask development 
and a Postgresql database) into a whole project as opposed to a disparate set of concepts, and at the same time create a 
resource someone might find useful. harvester.py gathers the data from the D.C. open data site, converts the location data 
from the given coordinate system to the more common latitude and longitude coordinates,and then uses the Google Maps api to 
reverse geocode those coordinates to standard addresses and stores that info in the database. aed.py is a Flask app built to 
access the aed info.



## Required to run:
Postgresql
Psycopg (`pip install psycopg2`)
PROJ4 (`pip install pyproj`)
pw.py (contains the user supplied Google Maps dev key and postgres db password)


## Project can be downloaded from:
https://github.com/MarvinPerry/dc_aed

## Author and contributors:
* **Marvin L. Perry**
* http://opendata.dc.gov/datasets/ae96db0a66914f05ab09c83f9e9df15f_9


## File List:

* ./static
* style.css
* ./templates
* by_date.html
* by_facility.html
* get_id.html
*	index.html
* multi.html
aed.py
harvester.py
pw.py
License.txt

Run harvester.py to get Washington’s current AED information from the Washington D.C. open data site(link this) and store it in your database.Running harvester.py will take some time to handle api calls and reverse geocoding, but after the first time, it only ever needs to be run as often as the registered AED data is updated, which is not very often.

When harvester.py has has finished. Run aed.py to begin the Flask app and in your web browser, open http://127.0.0.1:5000/ to use the project.

Licensing information: READ LICENSE (link this)



