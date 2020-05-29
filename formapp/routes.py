from formapp import app, db
from formapp.forms import AddUserForm
from formapp.user_database import User, SpecificDrug, Drug, specific_drug_check
from flask import render_template, request, redirect, session, url_for


# Tutaj też trzeba (chyba) umieścić ewntualne funkcje POST itd.

@app.route('/') # ten fragment przekierowuje do formularza HTML
def hello_world():
    print("Poszło hello_world")                             # info o odpaleniu stronki
                                # utworzenie bazy danych z tabelami określonymi w pliku user_database.py
    # has_children = User.selected_drugs.any()    # tutaj sprawdzam czy są relację i printuję w logu flaska
    # q = db.session.query(User, has_children)
    # for parent, has_children in q.all():
    #     print(parent, has_children)
    return render_template('welcome.html')


@app.route('/addUser', methods=['GET', 'POST'])
def addUser(): # to
    '''
    Tutaj tworzymy obiekt formularza wtf z pliku forms.py odpowiedzialny za dodawanie użytkownika,
    klasa formularza dokładniej opisana w pliku forms.py
    '''
    form = AddUserForm()
    '''Zapisujemy tutaj dane z bazy danych w postaci słownikowej (chyba tak to się nazywa) i dodajemy do formularza '''
    all_records = SpecificDrug.query.all()
    form.drugs.choices = [(drug_name.id, drug_name.name) for drug_name in all_records]

    '''Tutaj jest warunek, jesli przycisk sumbit został kliknięty dane z formularza są zapisywane'''
    if form.validate_on_submit():
        sex = form.sex.data
        city = form.city.data
        age = form.age.data
        drugs = form.data['drugs']

        #sprawdzono - działa
        '''po utworzeniu użytkownika w sesji zapisywany jest jego id oraz lista narkotyków którą zaznaczył'''
        user = User(sex,age,city)
        session['drugs'] = drugs
        # session['drugs'] = drugs
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        session['user_id'] = user.id
        '''przekierowanie do formularza z odpowiedziami'''
        drugs_dict = {}  # Słownik do wyświetlania nazw w formularzach, gdzie kluczem jest id drug
        for dr_id in drugs:
            drugs_dict[str(dr_id)] = all_records[dr_id-1].name #  id w formularzu zaczynają się od 0 nie od 1 jak w tabeli
        session["drugs_dict"] = drugs_dict
        session["current_drug"] = 0
        session["drug_list_len"] = len(drugs)
        print("Test:", session["drugs_dict"])
        return redirect('/drugForm')

    '''Zaciągnięty obiekt formularza przesyłamy do wyrenderowanego pliku html, '''
    return render_template('addUser.html', form=form)






''' Chwilowe zakomentowanie wersji'''
# @app.route('/firstForm') # wyświetlenie pierwszego formularza
# def show_firstForm():
#     return render_template('firstForm.html')    # renderowanie strony na podstawie pliku firstForm.html
#
#
# @app.route("/saveFirst", methods=['POST']) # zapisywanie tego co zostało wklepane do formularza
# def save_first_form():                     # (odpala akcję /save w formularzu)
#     age = request.form['age']              # bierze tablicę/słownik POST i przypisuje do zmiennej lokalnej wartosć
#     user = User("M", age, "Karakan")       # wpisaną przez użytkownika
#     user_selected = request.form
#     print(user_selected)             # sprawdzam co się wyświetla po zaznaczeniu checkbocksów
#     user_selected_dict = user_selected.to_dict()
#     print("Only keys:", user_selected_dict.keys())
#     db.session.add(user) # testowe dodatnie do bazy danych rekordu
#     print("Before flush:", user.id)
#     db.session.commit()
#     db.session.refresh(user)
#     user_id = user.id
#     print(user_id)
#     session["user_id"] = user_id           # używam sesji, bo POST działa tlyko dla wskazanych adresów
#     iterating_list = []
#     for word, el in user_selected_dict.items():
#         if word == "age":
#             continue
#         else:
#             iterating_list.append(el)
#
#     session["drug_list"] = iterating_list
#     session["drug_list_len"] = len(iterating_list)
#     session["current_drug"] = 0
#     return redirect('/drugForm')           # przekierowanie na adres /drugForm


@app.route('/drugForm')  # wyświetlenie drugiego formularza formularza
def show_drugForm():
    if session["current_drug"] == session["drug_list_len"]:
        session.clear
        return redirect('/')
    else:
        print("current:", session["current_drug"])
        print("drug list:", session['drugs'])
        return render_template('drugForm.html', value = session["drugs_dict"][str(session['drugs'][session["current_drug"]])])


@app.route('/saveDrug', methods=['POST'])   # zapisywanie tego co zostało wybrane w formularzu z konkretnym narkotykiem
def save_drug_form():
    print("Selected values list:", request.form)    # tutaj akurat sprawdzam co się wysyła/odbiera
    print("Example for 'damage':", request.form['damage'])
    print("It's type is:", type(int(request.form['damage'])))
    damage = int(request.form['damage'])
    f_damage = int(request.form['f_damage'])
    temp_drug_id = 1    # chwilowa zmienna id narkotyku, dopóki nie ma bazy z narkotykami
    temp_user_id = session["user_id"]
    print("Last user ID:", temp_user_id)
    drug = Drug(temp_drug_id, temp_user_id, damage, f_damage)  # utworzenie rekordu do bazy Drug
    db.session.add(drug)
    db.session.commit()
    session["current_drug"] += 1
    return redirect('/drugForm')    # powrót na stronę głóną


specific_drug_check() # tafunkcja robi to co kod poniżej (zostawiłem tutaj na zaś, wystarczy odkomentować)
# aha, jakby ktoś się dziwił czemu to jest tutaj, a nie w __init__.py
# to jest w tym miejscu, ponieważ cały ten plik (czyli routes.py) jest importowany
# na końcu pliku init. Gdyby osobno importować tam ta funkcję, to są problemy z importami

# rows = db.session.query(SpecificDrug).count()
# print("Current number of records in 'specific_drug':", rows)
# if rows == 14:      # proste zabezpieczenie, aby baza danych miała naszą liste narkotyków przy starcie
#     pass            # aplikacji. Prosta bo nie sprawdza na bieżaco, ani nie czy ktoś coś podmienił
# else:
#     db.session.query(SpecificDrug).delete()
#     d1 = SpecificDrug('Alkohol')  # Tworzę obiekty klasy Drug_name (rekordy tabeli)
#     d2 = SpecificDrug('Heroina')
#     d3 = SpecificDrug('Kokaina')
#     d4 = SpecificDrug('Metaamfetamina')
#     d5 = SpecificDrug('Tytoń')
#     d6 = SpecificDrug('Amfetamina')
#     d7 = SpecificDrug('Marihuana')
#     d8 = SpecificDrug('MDMA')
#     d9 = SpecificDrug('Mefedron')
#     d10 = SpecificDrug('LSD')
#     d11 = SpecificDrug('Psylocybina')
#     d12 = SpecificDrug('Ketamina')
#     d13 = SpecificDrug('DXM')
#     d14 = SpecificDrug('DMT')
#     db.session.add_all([d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14])
#     print("End of statement")
#     rows = db.session.query(SpecificDrug).count()
#     print("After adding all:", rows)
#     db.session.commit()