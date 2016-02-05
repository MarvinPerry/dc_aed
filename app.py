from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from pw import ALC


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

    def __init__(self, ident):
        self.ident = ident

    def __init__(self, acquired):
        self.acquired = acquired

    def __init__(self, facility):
        self.facility = facility

    def __init__(self, location):
        self.location = location

@app.route('/')
def index():
    aeds = Defibs.query.all()
    return render_template('index.html', aeds = aeds)






if __name__== "__main__":
    app.debug = True
    app.run()