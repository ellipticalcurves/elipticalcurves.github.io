from flask import Flask, redirect, url_for, render_template
#from flask_sqlalchemy import SQLAlchemy
from dash import Dash
import csv

server = Flask(__name__)
#server.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(server)

#class Youtube(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
# app = Dash(__name__, server=server, url_base_pathname='/ATM_Data_Anlaysis/')



@server.route("/")
@server.route("/home")
def home():
    return render_template("index.html")

@server.route("/scene")
def threes():
    return render_template("scene.html")

if __name__ == '__main__':
    server.run(debug=True, port=5000)
