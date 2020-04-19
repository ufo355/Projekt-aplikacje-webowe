from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from user_database import db
from sqlalchemy.ext.declarative import declared_attr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drug_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'


db = SQLAlchemy(app) #tworzenie obiektu bazy danych


class User(db.Model): # definiowanie tabeli
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.CHAR)
    age = db.Column(db.Integer)
    town = db.Column(db.String)

    def __init__(self, sex, age, town): # dodawanie danych do odpowiadających im pól
        self.sex = sex
        self.age = age
        self.town = town


class Gibon(db.Model): # definiowanie tabeli abstrakcyjnej do używek
    __abstract__ = True
    @declared_attr
    def person(cls):    # konieczna jest taka definicja dla klucza obcego
        return db.Column(db.Integer, db.ForeignKey('user_data.id'))
    frequency = db.Column(db.Integer)
    self_damage = db.Column(db.Integer)
    public_damage = db.Column(db.Integer)
    legality = db.Column(db.Integer)

    def __init__(self, frequency, self_damage, public_damage, legality): # dodawanie danych do odpowiadających im pól
        self.frequency = frequency
        self.self_damage = self_damage
        self.public_damage = public_damage
        self.legality = legality


class Muskatnuss(Gibon):        # przy każdej dziedzieczkonej klasie należy definiować osobny dla niej klucz główny
    __tablename__ = 'muskatnuss'
    id = db.Column(db.Integer, primary_key=True)


class Kakaonuss(Gibon):
    __tablename__ = 'kakaonuss'
    id = db.Column(db.Integer, primary_key=True)


db.create_all() # utworzenie bazy danych z tabelami określonymi powyżej
db.drop_all() # czyszczenie bazy (przy każdym odświerzeniu dodaje nowe rekordy)


@app.route('/')
def hello_world():
    print("Poszło") # info o odpaleniu stronki

    user = User('W', 22, 'Szczawnica') # utworzenie rekordu do tabeli User
    muskatnuss = Muskatnuss(10, 5, 8, 3) # utworzenie rekordu do tabeli Muskatnus
    kakaonuss = Kakaonuss(6, 6, 6, 6)
    db.session.add(user)    # INSERT'owanie rekordów do tabeli
    db.session.add(muskatnuss)
    db.session.add(kakaonuss)
    db.session.commit() # zatwierdzenie dodania rekordu (uzyskanie ID)

    return "Witaj świecie"


db.create_all()
if __name__ == '__main__':
    app.run()