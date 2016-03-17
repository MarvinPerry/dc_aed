from flask import Flask, render_template, request
import psycopg2
import datetime
import pdb

try:
    import pw.py
except:
    pass


#### Begining trace here ####
# pdb.set_trace()

###################################################################################################
#tries to create the connection to the database, and prints failure message if necessarry
try:
    conn = psycopg2.connect(database=AED, user=postgres, password=dbpass, host=host, port=port)
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


@aed.route('/search/', methods =['GET', 'POST'])
def search():
    if request.method == 'GET':

        SQL = "SELECT * FROM defibs"
        cur.execute(SQL)
        aeds = cur.fetchall()
        return render_template('index.html', aeds=aeds)


    if request.method == 'POST':

        if request.form['rbut'] == "ident" and request.form['field'] != "":

            data = (request.form['field'],)
            try:
                mapResults = request.form['mapResults']
            except:
                mapResults = False

            SQL = "SELECT * FROM defibs WHERE ident =(%s)"   
            cur.execute(SQL, data)
            usrAed = cur.fetchall()

            return render_template('results.html', data=data, mapResults=mapResults, usrAed=usrAed)
    

        
        if request.form['rbut'] == 'date':

            if request.form['startYr'] != "" and request.form['endYr'] != "":
                startYr = (request.form['startYr'].split("-"))
                endYr = (request.form['endYr'].split("-")) 
                
                print startYr, endYr

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
                SQL = "SELECT * FROM defibs"
                cur.execute(SQL)
                aeds = cur.fetchall()
                return render_template('index.html', aeds=aeds)

        

        if request.form['rbut'] == "facility" and request.form['field'] != "":


                try:
                    usrInput = request.form['field']
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

                    return render_template('results.html', soloFacil=soloFacil, usrFacil=usrFacil, count=count, usrInput=usrInput, mapResults=mapResults)
                
                except:
                    SQL = "SELECT * FROM defibs"
                    cur.execute(SQL)
                    aeds = cur.fetchall()
                    return render_template('index.html', aeds=aeds)

        else:
            SQL = "SELECT * FROM defibs"
            cur.execute(SQL)
            aeds = cur.fetchall() 
    
    return render_template('index.html', aeds=aeds)


if __name__== "__main__":
    # aed.debug = True
    aed.run()






























