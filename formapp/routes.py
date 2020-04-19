from formapp import app, db
from formapp.user_database import User, Gibon, Muskatnuss, Kakaonuss
# Tutaj też trzeba (chyba) umieścić ewntualne funkcje POST itd.

@app.route('/')
def hello_world():
    print("Poszło") # info o odpaleniu stronki
    db.create_all()  # utworzenie bazy danych z tabelami określonymi powyżej
    user = User('W', 22, 'Szczawnica') # utworzenie rekordu do tabeli User
    muskatnuss = Muskatnuss(10, 5, 8, 3) # utworzenie rekordu do tabeli Muskatnus
    kakaonuss = Kakaonuss(6, 6, 6, 6)
    db.session.add(user)    # INSERT'owanie rekordów do tabeli
    db.session.add(muskatnuss)
    db.session.add(kakaonuss)
    db.session.commit() # zatwierdzenie dodania rekordu (uzyskanie ID)

    return "Witaj świecie"