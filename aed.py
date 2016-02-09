from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from pw import ALC, dbpass



####################################################################################################
#write raw sql commands tomorrow
import psycopg2
#tries to create the connection to the database, and prints failure message if necessarry
try:
    conn = psycopg2.connect(database='AED', user='postgres', password=dbpass, host='127.0.0.1', port='5432')
    print "Connection successful"
except:
    print "Database connection failed."
#a cursor used to perform queries
cur = conn.cursor()
####################################################################################################

aed = Flask(__name__)

#setting up the database
aed.config['SQLALCHEMY_DATABASE_URI'] = ALC


# an instance of the database to interact with
db = SQLAlchemy(aed)


#setting up the database model where each field in the table must be represented 

class Defibs(db.Model):
    __tablename__= "defibs"
    ident = db.Column(db.Integer, primary_key=True, nullable=False)
    acquired = db.Column(db.BigInteger)
    facility = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text)
    brand = db.Column(db.Text)
    aed_model = db.Column(db.Text)
    aed_model_num = db.Column(db.Text)
    lng = db.Column(db.Numeric)
    lat = db.Column(db.Numeric)
    expires = db.Column(db.Text)
    replaced = db.Column(db.Text)


# index page that currently shows a record of every AED in the table
@aed.route('/')
def index():
    aeds = Defibs.query.all()
    return render_template('index.html', aeds = aeds)


# the page for users searching for one specific aed by id
@aed.route('/get_id', methods =['GET', 'POST'])
def get_id():
    
    if request.method == 'GET':
        
        return render_template('get_id.html')

    
    if request.method == 'POST':
        print "got here 2"

        SQL = "SELECT * FROM defibs WHERE ident =(%s) "
       
        if str(request.form['num']).isdigit() == True:
            data = (request.form['num'],)
        else:
            data = (1,)

        cur.execute(SQL, data)
        usrAed = cur.fetchall()
        return render_template('get_id.html', usrAed = usrAed)
        


#the page for users searching for a range of aeds, from 1 to the user entered number
@aed.route('/query', methods = ['GET', 'POST'])
def query():
    if request.method == 'GET':
        return render_template('query.html')

    if request.method == 'POST':
        print "got here 4"

        SQL = "SELECT * FROM defibs WHERE ident <=(%s) "

        if str(request.form['num']).isdigit() == True:
            data = (request.form['num'],)
        else:
            data = (1,)
        cur.execute(SQL, data)
        usrAed = cur.fetchall()
        return render_template('query.html', usrAed = usrAed)




if __name__== "__main__":
    aed.debug = True
    aed.run()































