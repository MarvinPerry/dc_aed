from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from pw import ALC, dbpass
from datetime import datetime
import pdb
#### Begining trace here #####
# pdb.set_trace()



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
#########################################################################################


# the page for users searching for one specific aed by id
# @aed.route('/aed_id/')
@aed.route('/get_id/', methods=['GET', 'POST'])
@aed.route('/get_id/<int:num>', methods=['GET', 'POST'])

def get_id(num=None):
    if request.method == 'GET' and num == None:
        
        print "testing here 0"
        return render_template('get_id.html')

    elif request.method == 'POST':
        print "testing here 1"
        num=request.form['num']
        # pdb.set_trace()

        data = (request.form['num'],)
        SQL = "SELECT * FROM defibs WHERE ident =(%s)"   
        cur.execute(SQL, data)
        usrAed = cur.fetchall()
        # passing in num and usrAed to the singular aed page
        return render_template('get_id.html', num=num, usrAed=usrAed)

    else:
        print "testing here 2"
        return render_template('get_id.html')


#########################################################################################

# @aed.route('/aed_id/')
# def show_id():
#     return render_template('aed_id.html')
  
        
#########################################################################################


#the page for users searching for a range of aeds, from 1 to the user entered number



@aed.route('/by_facility', methods= ['GET', 'POST'])
def by_facility():
    if request.method =='GET':

        cur.execute("SELECT DISTINCT facility FROM defibs ORDER BY facility")
        print "after sql request"
        distFacil = cur.fetchall()
        return render_template('by_facility.html', distFacil=distFacil)
    

    if request.method == 'POST':
        try:
            soloFacil = request.form['Facility']
            print soloFacil
        except Exception as E:
            print str(E)
        
        
        return render_template('by_facility.html', soloFacil=soloFacil)


#########################################################################################


@aed.route('/query', methods = ['GET', 'POST'])
def query():
    if request.method == 'GET':
        try:
            print request.form['Facility']
        except:
            pass
        return render_template('query.html')


    if request.method == 'POST':

        SQL = "SELECT * FROM defibs WHERE ident <=(%s) "

        if str(request.form['num']).isdigit() == True:
            data = (request.form['num'],)
        else:
            data = (1,)
        cur.execute(SQL, data)
        usrAed = cur.fetchall()
        return render_template('query.html', usrAed=usrAed, data=data)



#########################################################################################

@aed.route('/queryrange', methods =['GET', 'POST'])
def queryrange():
    if request.method == 'GET':
    
        return render_template('queryrange.html')

    if request.method=='POST':
        if request.form['endYr'] != None and request.form['startYr'] != None:
            endYr = (request.form['endYr']) 
            startYr = (request.form['startYr'])

            print startYr
            print endYr

            # cur.execute("SELECT * from defibs WHERE DATE BETWEEN startYr and endYr ")
            # rangAed = cur.fetchall()
        return render_template('queryrange.html')#, rangAed=rangAed)

    else:
        return render_template('queryrange.html')




if __name__== "__main__":
    aed.debug = True
    aed.run()































