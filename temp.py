from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import psycopg2
from pw import ALC, dbpass
from datetime import datetime



try:
    conn = psycopg2.connect(database='AED', user='postgres', password=dbpass, host='127.0.0.1', port='5432')
    print "Connection successful"
except:
    print "Database connection failed."
#a cursor used to perform queries
cur = conn.cursor()



####this is test code to come up with a solution for converting the date###