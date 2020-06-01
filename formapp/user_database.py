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

    def __init__(self, name):# dodawanie nazw do odpowiadających im pól
        self.name = name


'''Tabela z odpowiedzi na pytnania w formularzu drugQuestionsForm. Obliczenia średnich ważonych
   znajdują się w definicji kostruktora (który zapisuje dane do tej tabeli już w bazie dancyh)'''


class Drug(db.Model): # tabela z wynikamoi na odpowiedzi do pytań i narkotyków
    __tablename__ = 'drug'
    id = db.Column(db.Integer, primary_key=True)
    id_drug = db.Column(db.Integer, db.ForeignKey("specific_drug.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user_data.id"))
    '''Kryteria na szkodliwość biorącego'''
    crit_1 = db.Column(db.Integer)
    crit_2 = db.Column(db.Integer)
    crit_3 = db.Column(db.Integer)
    crit_4 = db.Column(db.Integer)
    crit_5 = db.Column(db.Integer)
    crit_6 = db.Column(db.Integer)
    crit_7 = db.Column(db.Integer)
    crit_8 = db.Column(db.Integer)
    crit_9 = db.Column(db.Integer)
    crit_10 = db.Column(db.Integer)
    crit_11 = db.Column(db.Integer)
    crit_12 = db.Column(db.Integer)
    '''Od tego momentu sa kryteria na szkodliwośc społeczną'''
    crit_13 = db.Column(db.Integer)
    crit_14 = db.Column(db.Integer)
    crit_15 = db.Column(db.Integer)
    crit_16 = db.Column(db.Integer)
    crit_17 = db.Column(db.Integer)
    crit_18 = db.Column(db.Integer)
    self_dmg_weight_avg = db.Column(db.Float)
    society_dmg_weight_avg = db.Column(db.Float)

    def __init__(self, id_drug, id_user, crit_1, crit_2, crit_3, crit_4, crit_5, crit_6, crit_7, crit_8, crit_9, crit_10, crit_11, crit_12, crit_13, crit_14, crit_15, crit_16, crit_17, crit_18):
        self.id_drug = id_drug
        self.id_user = id_user
        self.crit_1 = crit_1
        self.crit_2 = crit_2
        self.crit_3 = crit_3
        self.crit_4 = crit_4
        self.crit_5 = crit_5
        self.crit_6 = crit_6
        self.crit_7 = crit_7
        self.crit_8 = crit_8
        self.crit_9 = crit_9
        self.crit_10 = crit_10
        self.crit_11 = crit_11
        self.crit_12 = crit_12
        self.crit_13 = crit_13
        self.crit_14 = crit_14
        self.crit_15 = crit_15
        self.crit_16 = crit_16
        self.crit_17 = crit_17
        self.crit_18 = crit_18
        '''Tutaj bd dłuuuugaśnie obliczenia'''
        self.self_dmg_weight_avg = crit_1 * 0.2 + crit_2 * 0.15 + crit_3 * 0.15 + crit_4 * 0.12 + crit_5 * 0.12 + crit_6 * 0.08 + crit_7 * 0.05 + crit_8 * 0.05 + crit_9 * 0.04 + crit_10 * 0.03 + crit_11 * 0.007 + crit_12 * 0.003
        self.society_dmg_weight_avg = crit_13 * 0.5 + crit_14 * 0.3 + crit_15 * 0.15 + crit_16 * 0.03 + crit_17 * 0.015 + crit_18 * 0.005


def specific_drug_check():
    rows = db.session.query(SpecificDrug).count()
    print("Current number of records in 'specific_drug':", rows)
    if rows == 14:  # proste zabezpieczenie, aby baza danych miała naszą liste narkotyków przy starcie
        pass  # aplikacji. Prosta bo nie sprawdza na bieżaco, ani nie czy ktoś coś podmienił
    else:
        db.session.query(SpecificDrug).delete()
        d1 = SpecificDrug('Alkohol')  # Tworzę obiekty klasy Drug_name (rekordy tabeli)
        d2 = SpecificDrug('Heroina')
        d3 = SpecificDrug('Kokaina')
        d4 = SpecificDrug('Metaamfetamina')
        d5 = SpecificDrug('Tytoń')
        d6 = SpecificDrug('Amfetamina')
        d7 = SpecificDrug('Marihuana')
        d8 = SpecificDrug('MDMA')
        d9 = SpecificDrug('Mefedron')
        d10 = SpecificDrug('LSD')
        d11 = SpecificDrug('Psylocybina')
        d12 = SpecificDrug('Ketamina')
        d13 = SpecificDrug('DXM')
        d14 = SpecificDrug('DMT')
        db.session.add_all([d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14])
        print("End of statement")
        rows = db.session.query(SpecificDrug).count()
        print("After adding all:", rows)
        db.session.commit()


''' Zostawiam w razie czego, może się przyda klasa (tabel) abstracyjna jeszcze '''

# class Gibon(db.Model): # definiowanie Klasy tabeli abstrakcyjnej do używek
#     __abstract__ = True
#     @declared_attr
#     def person(cls):    # konieczna jest taka definicja dla klucza obcego
#         return db.Column(db.Integer, db.ForeignKey('user_data.id'))
#     frequency = db.Column(db.Integer)
#     self_damage = db.Column(db.Integer)
#     public_damage = db.Column(db.Integer)
#     legality = db.Column(db.Integer)
#
#     def __init__(self, frequency, self_damage, public_damage, legality): # dodawanie danych do odpowiadających im pól
#         self.frequency = frequency
#         self.self_damage = self_damage
#         self.public_damage = public_damage
#         self.legality = legality
#
#
# class Muskatnuss(Gibon):        # przy każdej dziedzieczkonej klasie należy definiować osobny dla niej klucz główny
#     __tablename__ = 'muskatnuss'
#     id = db.Column(db.Integer, primary_key=True)
#
#
# class Kakaonuss(Gibon):
#     __tablename__ = 'kakaonuss'
#     id = db.Column(db.Integer, primary_key=True)



