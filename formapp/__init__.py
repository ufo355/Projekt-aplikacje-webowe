from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from user_database import db
from sqlalchemy.ext.declarative import declared_attr

# Tutaj należy umieścić importy do formularza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drug_database.db'  # utworzenie ścieżki do pliku bazy danych
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)  # tworzenie obiektu bazy danych

from formapp import routes
