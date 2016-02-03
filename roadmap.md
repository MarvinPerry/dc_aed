1. Query DC’s  ARC GIS  site for the AED data

- This API call shouldn’t be made for each user since the data doesn’t seem to be updated frequently. When the API call is made initially it should be flagged with date of the request. When a new user requests the data the current time and the time of the last request should be compared, and if a sufficient amount of time has passed, the API call should be made again, and the dataset and the date stamp updated. 




2. Store that data in a Postgres DB:

2a: Convert the location data into format compatible with a leaflet map.  



id(primary key). (integer)

facility name,(string)

location (string)

x coord (double precision, or  maybe real after conversion)

y coord (double precision, or  maybe real after conversion)

expiration date (date)

replaced(string)

brand (string)

model(string



3. Build a Flask site that let’s users query my db and displays the data in a plain text on the page.

-Queries would be via webform






next goals:

Take the raw results and format it in a more useable way to allow for sorting it in ascending and descending order without having to query the db again. This means html and some javascript(?)