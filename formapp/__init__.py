from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
# from formapp.user_database import SpecificDrug
from sqlalchemy.ext.declarative import declared_attr

# Tutaj należy umieścić importy do formularza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drug_database.db'  # utworzenie ścieżki do pliku bazy danych
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True' # to jest chyba do debbugowania
app.secret_key = "69twoja_stara420" # klucz potrzebny do sesji
db = SQLAlchemy(app)  # tworzenie obiektu bazy danych
print("Start")

from formapp import routes # tutaj teoretycznie wczytuje się ten plik routes i tak jakby pod tym jest cały kompletny skrypt pajtona
                           # więc pewnie tutaj trzeba inicjalizowac bazy danych
''' UWAGA!!! - przeniesione db.createAll() do routes, było to konieczne, bo tworzyło bazę dopiero po wszytkich liniach
kodu pliku routes. Teraz jest tam na początku o wszystko działą cacy'''

