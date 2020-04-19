from sqlalchemy.ext.declarative import declared_attr

from formapp import db



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



