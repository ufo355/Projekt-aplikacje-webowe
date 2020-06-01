from formapp import app, db
from formapp.forms import AddUserForm
from formapp.user_database import User, SpecificDrug, Drug, specific_drug_check
from flask import render_template, request, redirect, session, url_for


# Tutaj też trzeba (chyba) umieścić ewntualne funkcje POST itd.\
db.create_all()
@app.route('/') # ten fragment przekierowuje do formularza HTML
def hello_world():
    print("Poszło hello_world")                             # info o odpaleniu stronki
                                # utworzenie bazy danych z tabelami określonymi w pliku user_database.py
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
        return redirect('/drugQuestionsForm')

    '''Zaciągnięty obiekt formularza przesyłamy do wyrenderowanego pliku html, '''
    return render_template('addUser.html', form=form)


@app.route('/drugQuestionsForm')  # wyświetlenie drugiego formularza formularza
def show_drugQuestionsForm():
    if session["current_drug"] == session["drug_list_len"]:
        session.clear
        return redirect('/')
    else:
        print("current drug:", session['drugs'][session["current_drug"]])
        print("drug list:", session['drugs']) # wyświetla numety jak w bazie dancyh, wybranych narkotyków
        return render_template('drugQuestionsForm.html', value = session["drugs_dict"][str(session['drugs'][session["current_drug"]])])


@app.route('/saveDrugQuestions', methods=['POST'])   # zapisywanie tego co zostało wybrane w formularzu z konkretnym narkotykiem
def save_drug_form():
    print("Selected values list:", request.form)    # tutaj akurat sprawdzam co się wysyła/odbiera
    print("Example for 'crit_1':", request.form['crit_1'])
    print("It's type is:", type(int(request.form['crit_1'])))
    '''Szkodliwość dla organizmu'''
    crit_1 = int(request.form['crit_1'])
    crit_2 = int(request.form['crit_2'])
    crit_3 = int(request.form['crit_3'])
    crit_4 = int(request.form['crit_4'])
    crit_5 = int(request.form['crit_5'])
    crit_6 = int(request.form['crit_6'])
    crit_7 = int(request.form['crit_7'])
    crit_8 = int(request.form['crit_8'])
    crit_9 = int(request.form['crit_9'])
    crit_10 = int(request.form['crit_10'])
    crit_11 = int(request.form['crit_11'])
    crit_12 = int(request.form['crit_12'])
    '''Skodliwość dla społeczeństwa'''
    crit_13 = int(request.form['crit_13'])
    crit_14 = int(request.form['crit_14'])
    crit_15 = int(request.form['crit_15'])
    crit_16 = int(request.form['crit_16'])
    crit_17 = int(request.form['crit_17'])
    crit_18 = int(request.form['crit_18'])
    temp_drug_id = session['drugs'][session["current_drug"]]  # zapisywanie id substancji
    temp_user_id = session["user_id"]   # zapisywanie id aktualnego użytkownika
    print("Last user ID:", temp_user_id)
    drug = Drug(temp_drug_id, temp_user_id, crit_1, crit_2, crit_3, crit_4, crit_5, crit_6, crit_7, crit_8, crit_9, crit_10, crit_11, crit_12, crit_13, crit_14, crit_15, crit_16, crit_17, crit_18)  # utworzenie rekordu do bazy Drug
    db.session.add(drug)
    db.session.commit()
    session["current_drug"] += 1
    return redirect('/drugQuestionsForm')    # powrót na stronę głóną


specific_drug_check() # tafunkcja robi to co kod poniżej (zostawiłem tutaj na zaś, wystarczy odkomentować)
# aha, jakby ktoś się dziwił czemu to jest tutaj, a nie w __init__.py
# to jest w tym miejscu, ponieważ cały ten plik (czyli routes.py) jest importowany
# na końcu pliku init. Gdyby osobno importować tam ta funkcję, to są problemy z importami

