from formapp import app, db
from formapp.user_database import User, Gibon, Muskatnuss, Kakaonuss, SpecificDrug, Drug
from flask import render_template, request, redirect


# Tutaj też trzeba (chyba) umieścić ewntualne funkcje POST itd.

@app.route('/') # ten fragment przekierowuje do formularza HTML
def hello_world():
    print("Poszło") # info o odpaleniu stronki
    db.create_all()  # utworzenie bazy danych z tabelami określonymi powyżej
    # user = User('W', 22, 'Szczawnica') # utworzenie rekordu do tabeli User
    # muskatnuss = Muskatnuss(10, 5, 8, 3) # utworzenie rekordu do tabeli Muskatnus
    # kakaonuss = Kakaonuss(6, 6, 6, 6)
    # db.session.add(user)    # INSERT'owanie rekordów do tabel
    # db.session.add(muskatnuss)
    # db.session.add(kakaonuss)
    # db.session.commit() # zatwierdzenie dodania rekordów (uzyskanie ID)

    return render_template('form.html')

@app.route("/save", methods=['POST']) # zapisywanie tego co zostało wklepane do formularza (odpala akcję /save w formularzu)
def save():
    age = request.form['age']
    user = User("M", age, "Karakan")
    selected_drugs_list = request.form
    print(selected_drugs_list)
    db.session.add(user) # testowe dodatnie do bazy danych rekordu
    db.session.commit()
    return redirect('/')
