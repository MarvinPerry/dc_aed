from flask import Flask, render_template, request
import psycopg2
from pw import dbpass, googMapKey
import datetime
import pdb

#### Begining trace here #####
# pdb.set_trace()

####################################################################################################
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

# index page that currently shows a record of every AED in the table
@aed.route('/')
def index():

    SQL = "SELECT * FROM defibs"
    cur.execute(SQL)
    aeds = cur.fetchall() 
    
    return render_template('index.html', aeds=aeds)
#################################################################################################


# the page for users searching for one specific aed by id
@aed.route('/get_id/', methods=['GET', 'POST'])
def get_id():

    if request.method == 'GET':
        
        return render_template('get_id.html')

    elif request.method == 'POST' and request.form['num'].isdigit() == True: 
        data = (request.form['num'],)

        try:
            mapResults = request.form['mapResults']
        except:
            mapResults = False


        SQL = "SELECT * FROM defibs WHERE ident =(%s)"   
        cur.execute(SQL, data)
        usrAed = cur.fetchall()
        
        # passing in num and usrAed to the page
        return render_template('get_id.html', usrAed=usrAed, mapResults=mapResults)

    else:
        return render_template('get_id.html')

        
#########################################################################################
#the page for users searching for AEDs by facility

@aed.route('/by_facility/', methods= ['GET', 'POST'])
def by_facility():
    if request.method =='GET':
        cur.execute("SELECT DISTINCT facility FROM defibs ORDER BY facility")
        distFacil = cur.fetchall()
        return render_template('by_facility.html', distFacil=distFacil)
    


    if request.method == 'POST':
        if request.form['facilNameTypd'] != "":
            
            try:
                usrInput = request.form['facilNameTypd']
                soloFacil = ('%'+ usrInput + '%')
                data = (soloFacil,) #puts the facility returned from the form in a tuple named data

                #assigns the SQL command to a variable named SQL with a variable placeholder in the form of %s
                #which is then all passed into cur.execute and run, with the results being assigned to usrFacil
            
                SQL = "SELECT * FROM defibs WHERE facility::text ILIKE (%s)"   
                cur.execute(SQL, data)
                usrFacil = cur.fetchall()
                count = len(usrFacil)

                try:
                    mapResults = request.form['mapResults']
                except:
                    mapResults = False

                return render_template('by_facility.html', soloFacil=soloFacil, usrFacil=usrFacil, count=count, usrInput=usrInput, mapResults=mapResults)
            
            except Exception as E:
                print str(E)

            
        elif request.form['facilNameTypd'] == "":
            facilNameTypd = request.form['facilNameTypd']
            return render_template('by_facility.html', facilNameTypd=facilNameTypd)


        
        


#########################################################################################
#the page for users searching for a range of AEDs, from 1 to the user entered number

@aed.route('/multi/', methods = ['GET', 'POST'])
def multi():
    if request.method == 'GET':
        count = None
        return render_template('multi.html', count=count)


    if request.method == 'POST':
        count = 0
        try:
            mapResults = request.form['mapResults']
        except:
            mapResults = False

        SQL = "SELECT * FROM defibs WHERE ident <=(%s) "

        if str(request.form['num']).isdigit() == True:
            data = (request.form['num'],)
            cur.execute(SQL, data)
            usrAed = cur.fetchall()
            count = len(usrAed)
            return render_template('multi.html', usrAed=usrAed, data=data, count=count, mapResults=mapResults)
        elif str(request.form['num']).isdigit() != True:
            return render_template('multi.html', count=count)

        # data = (1,)
            



#########################################################################################

@aed.route('/by_date/', methods =['GET', 'POST'])
def by_date():
    if request.method == 'GET':
    
        return render_template('by_date.html')

    if request.method=='POST':
        if request.form['endYr'] != "" and request.form['startYr'] != "":

            startYr = (request.form['startYr'].split("-"))
            endYr = (request.form['endYr'].split("-")) 
            
            #converts the user entered years from the form to python date objects
            startYr = datetime.date(int(startYr[0]),int(startYr[1]),int(startYr[2]))
            endYr = datetime.date(int(endYr[0]),int(endYr[1]),int(endYr[2]))
            try:
                mapResults = request.form['mapResults']
            except:
                mapResults = False
                
            SQL = "SELECT * from defibs WHERE acquired BETWEEN %s and %s"
            dates = (startYr, endYr)

            cur.execute(SQL,dates)
            rangAed = cur.fetchall()
            return render_template('by_date.html', rangAed=rangAed, startYr=startYr, endYr=endYr, mapResults=mapResults)
        else:
            return render_template('by_date.html')

    else:
        return render_template('by_date.html')

#########################################################################################

if __name__== "__main__":
    aed.debug = True
    aed.run()






























