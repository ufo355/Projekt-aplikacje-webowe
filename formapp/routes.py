from formapp import app, db
from formapp.user_database import User, SpecificDrug, Drug
from flask import render_template, request, redirect, session


# Tutaj też trzeba (chyba) umieścić ewntualne funkcje POST itd.

@app.route('/') # ten fragment przekierowuje do formularza HTML
def hello_world():
    print("Poszło")                             # info o odpaleniu stronki
    db.create_all()                             # utworzenie bazy danych z tabelami określonymi w pliku user_database.py
    # has_children = User.selected_drugs.any()    # tutaj sprawdzam czy są relację i printuję w logu flaska
    # q = db.session.query(User, has_children)
    # for parent, has_children in q.all():
    #     print(parent, has_children)
    return render_template('welcome.html')


@app.route('/firstForm') # wyświetlenie pierwszego formularza
def show_firstForm():
    return render_template('firstForm.html')    # renderowanie strony na podstawie pliku firstForm.html


@app.route("/saveFirst", methods=['POST']) # zapisywanie tego co zostało wklepane do formularza
def save_first_form():                     # (odpala akcję /save w formularzu)
    age = request.form['age']              # bierze tablicę/słownik POST i przypisuje do zmiennej lokalnej wartosć
    user = User("M", age, "Karakan")       # wpisaną przez użytkownika
    user_selected = request.form
    print(user_selected)             # sprawdzam co się wyświetla po zaznaczeniu checkbocksów
    user_selected_dict = user_selected.to_dict()
    print("Only keys:", user_selected_dict.keys())
    db.session.add(user) # testowe dodatnie do bazy danych rekordu
    print("Before flush:",user.id)
    db.session.commit()
    db.session.refresh(user)
    user_id = user.id
    print(user_id)
    session["user_id"] = user_id           # używam sesji, bo POST działa tlyko dla wskazanych adresów
    iterating_list = []
    for word, el in user_selected_dict.items():
        if word == "age":
            continue
        else:
            iterating_list.append(el)

    session["drug_list"] = iterating_list
    session["drug_list_len"] = len(iterating_list)
    session["current_drug"] = 0
    return redirect('/drugForm')           # przekierowanie na adres /drugForm


@app.route('/drugForm')  # wyświetlenie drugiego formularza formularza
def show_drugForm():
    if session["current_drug"] == session["drug_list_len"]:
        return redirect('/')
    else:
        return render_template('drugForm.html', value = session["drug_list"][session["current_drug"]])


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
    session["current_drug"] += 1
    return redirect('/drugForm')    # powrót na stronę głóną
