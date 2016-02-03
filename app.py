from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
#setting up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'

# an instance of the database to interact with
db = SQLAlchemy(app)


#setting up the database model where each field in the table must be represented 

class AED(db.Model):
    __tablename__= "aed"
    ident = db.Column(db.Integer, primary_key=True)
    acquired = db.Column(db.Integer)
    facility = db.Column(db.string)
    location = db.Column(db.string)
    brand = db.Column(db.string)
    model = db.Column(db.string)
    model_num = db.Column(db.string)
    x_cord = db.Column(db.string)
    y_cord = db.Column(db.string)
    expire = db.Column(db.string)
    replaced = db.Column(db.string)

    def __init__(self, ident)