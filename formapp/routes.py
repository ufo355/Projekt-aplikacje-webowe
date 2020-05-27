from formapp import app, db
from formapp.user_database import User, SpecificDrug, Drug
from flask import render_template, request, redirect


# Tutaj też trzeba (chyba) umieścić ewntualne funkcje POST itd.

@app.route('/') # ten fragment przekierowuje do formularza HTML
def hello_world():
    print("Poszło")                             # info o odpaleniu stronki
    db.create_all()                             # utworzenie bazy danych z tabelami określonymi w pliku user_database.py
    has_children = User.selected_drugs.any()    # tutaj sprawdzam czy są relację i printuję w logu flaska
    q = db.session.query(User, has_children)
    for parent, has_children in q.all():
        print(parent, has_children)
    return render_template('welcome.html')


@app.route('/firstForm') # wyświetlenie pierwszego formularza
def show_firstForm():
    return render_template('firstForm.html')    # renderowanie strony na podstawie pliku firstForm.html


@app.route("/saveFirst", methods=['POST']) # zapisywanie tego co zostało wklepane do formularza
def save_first_form():                     # (odpala akcję /save w formularzu)
    age = request.form['age']              # bierze tablicę/słownik POST i przypisuje do zmiennej lokalnej wartosć
    user = User("M", age, "Karakan")       # wpisaną przez użytkownika
    selected_drugs_list = request.form
    print(selected_drugs_list)             # sprawdzam co się wyświetla po zaznaczeniu checkbocksów
    db.session.add(user) # testowe dodatnie do bazy danych rekordu
    db.session.commit()
    return redirect('/drugForm')           # przekierowanie na adres /drugForm


@app.route('/drugForm') # wyświetlenie drugiego formularza formularza
def show_drugtForm():
    return render_template('drugForm.html')


@app.route('/saveDrug', methods=['POST'])   # zapisywanie tego co zostało wybrane w formularzu z konkretnym narkotykiem
def save_drug_form():
    print("Selected values list:", request.form)    # tutaj akurat sprawdzam co się wysyła/odbiera
    print("Example for 'damage':", request.form['damage'])
    print("It's type is:", type(int(request.form['damage'])))
    damage = int(request.form['damage'])
    f_damage = int(request.form['f_damage'])
    temp_drug_id = 1    # chwilowa zmienna id narkotyku, dopóki nie ma bazy z narkotykami
    last_user_record = db.session.query(User).order_by(User.id.desc()).first() # wybranie ostatnio doadanego użytkowniaka
    temp_user_id = last_user_record.id # wydobycie id od niego
    print("Last user ID:", temp_user_id)
    drug = Drug(temp_drug_id, temp_user_id, damage, f_damage)  # utworzenie rekordu do bazy Drug
    db.session.add(drug)
    db.session.commit()
    return redirect('/')    # powrót na stronę głóną
