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

app = Flask(__name__)

#setting up the database
app.config['SQLALCHEMY_DATABASE_URI'] = ALC


# an instance of the database to interact with
db = SQLAlchemy(app)


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
    x_cord = db.Column(db.Numeric)
    y_cord = db.Column(db.Numeric)
    expires = db.Column(db.Text)
    replaced = db.Column(db.Text)


    # def __init__(self, ident):
    #     self.ident = ident

    # def __init__(self, acquired):
    #     self.acquired = acquired

    # def __init__(self, facility):
    #     self.facility = facility

    # def __init__(self, location):
    #     self.location = location


@app.route('/')
def index():
    aeds = Defibs.query.all()
    return render_template('index.html', aeds = aeds)









@app.route('/get_id', methods =['GET', 'POST'])
def get_id():
    
    if request.method == 'GET':
        print "got here 1"
        return render_template('get_id.html')

    
    if request.method == 'POST':
        print "got here 2"

        SQL = "SELECT * FROM defibs WHERE ident =(%s) "
        data = (request.form['num'],)
        cur.execute(SQL, data)
        usrAed = cur.fetchall()
        return render_template('get_id.html', usrAed = usrAed)









@app.route('/query', methods = ['GET', 'POST'])
def query():
    if request.method == 'GET':
        print "got here 3"
        return render_template('query.html')

    if request.method == 'POST':
        print "got here 4"

        SQL = "SELECT * FROM defibs WHERE ident <=(%s) "
        data = (request.form['num'],)
        cur.execute(SQL, data)
        usrAed = cur.fetchall()
        return render_template('query.html', usrAed = usrAed)




if __name__== "__main__":
    app.debug = True
    app.run()































