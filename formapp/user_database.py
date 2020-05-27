from sqlalchemy.ext.declarative import declared_attr

from formapp import db # import obiektu db z pliku __init__.py



class User(db.Model): # definiowanie tabeli
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.CHAR)
    town = db.Column(db.String)
    age = db.Column(db.Integer)
    selected_drugs = db.relationship("Drug", backref= "user_data")

    def __init__(self, sex, age, town): # dodawanie danych do odpowiadających im pól
        self.sex = sex
        self.age = age
        self.town = town


class SpecificDrug(db.Model): # definiowanie tabeli z naszymi narkotykami
    __tablename__ = 'specific_drug'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    drug_prop = db.relationship("Drug", backref= "specific_drug")

    def __init__(self, name):# dodawanie danych do odpowiadających im pól
        self.name = name

class Drug(db.Model):
    __tablename__ = 'drug'
    id = db.Column(db.Integer, primary_key=True)
    id_drug = db.Column(db.Integer, db.ForeignKey("specific_drug.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user_data.id"))
    damage = db.Column(db.Integer)
    familly_damage = db.Column(db.Integer)
    self_avg = db.Column(db.Float)
    society_avg = db.Column(db.Float)

    def __init__(self, id_drug, id_user, damage, familly_damage):
        self.id_drug = id_drug
        self.id_user = id_user
        self.damage = damage
        self.familly_damage = familly_damage
        self.self_avg = damage * 0.5
        self.society_avg= familly_damage * 0.7


class Gibon(db.Model): # definiowanie Klasy tabeli abstrakcyjnej do używek
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



