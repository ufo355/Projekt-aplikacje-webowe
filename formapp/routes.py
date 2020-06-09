from formapp import app
from formapp.forms import AddUserForm
from formapp.user_database import User, SpecificDrug, Drug, specific_drug_check
from flask import render_template, request, redirect, session, url_for
import numpy as np


# Tutaj też trzeba (chyba) umieścić ewntualne funkcje POST itd.\
#db.create_all()

#specific_drug_check() # tafunkcja robi to co kod poniżej (zostawiłem tutaj na zaś, wystarczy odkomentować)
# aha, jakby ktoś się dziwił czemu to jest tutaj, a nie w __init__.py
# to jest w tym miejscu, ponieważ cały ten plik (czyli routes.py) jest importowany
# na końcu pliku init. Gdyby osobno importować tam ta funkcję, to są problemy z importami


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


@app.route('/list', methods=['GET', 'POST'])
def list():
    print('Wyswietlanie wynikow')
    drugs = ['Alkohol','Heroina','Kokaina','Metaamfetamina','Tytoń','Amfetamina','Marihuana','MDMA','Mefedron','LSD','Psylocybina','Ketamina','DXM','DMT']
    self_damage_average = []
    society_damage_average = []
    number_of_drugs = []

    for drug in drugs:
        drugID = SpecificDrug.query.filter_by(name=drug).first().id
        recordsInDrug = Drug.query.filter_by(id_drug=drugID).all()
        number = len(recordsInDrug)
        number_of_drugs.append([drug,number])
        meansself = []
        meanssocity = []
        for record in recordsInDrug:
            meansself.append(record.self_dmg_weight_avg)
            meanssocity.append(record.society_dmg_weight_avg)
        
        self_damage_average.append([drug,np.mean(meansself)])
        society_damage_average.append([drug,np.mean(meanssocity)])
      
    return render_template('Result.html',self_damage_average = self_damage_average, society_damage_average = society_damage_average, number_of_drugs = number_of_drugs)

@app.route('/info', methods=['GET', 'POST'])
def info():
    '''strona z informacjami o ankiecie'''
    return render_template('info.html')


    # alcohol = 0
    # cocaine = 0
    # heroine = 0
    # meta = 0
    # tobacco = 0
    # amfa = 0
    # marihuana = 0
    # mdma = 0
    # mefedron = 0
    # lsd = 0
    # psylocibine = 0
    # ketamine = 0
    # dxm = 0
    # dmt = 0
    # alcohol_self_dmg = 0
    # alcohol_self_avg = 0
    # alcohol_society = 0
    # alcohol_society_avg = 0
    # heroine_self_dmg = 0
    # heroine_self_avg = 0
    # heroine_society = 0
    # heroine_society_avg = 0
    # cocaine_self_dmg = 0
    # cocaine_self_avg = 0
    # cocaine_society = 0
    # cocaine_society_avg = 0
    # meta_self_dmg = 0
    # meta_self_avg = 0
    # meta_society = 0
    # meta_society_avg = 0
    # tobacco_self_dmg = 0
    # tobacco_self_avg = 0
    # tobacco_society = 0
    # tobacco_society_avg = 0
    # amfa_self_dmg = 0
    # amfa_self_avg = 0
    # amfa_society = 0
    # amfa_society_avg = 0
    # marihuana_self_dmg = 0
    # marihuana_self_avg = 0
    # marihuana_society = 0
    # marihuana_society_avg = 0
    # mdma_self_dmg = 0
    # mdma_self_avg = 0
    # mdma_society = 0
    # mdma_society_avg = 0
    # mefedron_self_dmg = 0
    # mefedron_self_avg = 0
    # mefedron_society = 0
    # mefedron_society_avg = 0
    # lsd_self_dmg = 0
    # lsd_self_avg = 0
    # lsd_society = 0
    # lsd_society_avg = 0
    # psylocibine_self_dmg = 0
    # psylocibine_self_avg = 0
    # psylocibine_society = 0
    # psylocibine_society_avg = 0
    # ketamine_self_dmg = 0
    # ketamine_self_avg = 0
    # ketamine_society = 0
    # ketamine_society_avg = 0
    # dxm_self_dmg = 0
    # dxm_self_avg = 0
    # dxm_society = 0
    # dxm_society_avg = 0
    # dmt_self_dmg = 0
    # dmt_self_avg = 0
    # dmt_society = 0
    # dmt_society_avg = 0
    # result = Drug.query.all()
    # for i in result:
    #     if i.id_drug == 1:
    #         alcohol += 1
    #         alcohol_self_dmg += i.self_dmg_weight_avg
    #         alcohol_self_avg = alcohol_self_dmg/alcohol
    #         alcohol_society += i.society_dmg_weight_avg
    #         alcohol_society_avg = alcohol_society/alcohol
    #     else:
    #         alcohol += 0


    # for i in result:
    #     if i.id_drug == 2:
    #         heroine += 1
    #         heroine_self_dmg += i.self_dmg_weight_avg
    #         heroine_self_avg = heroine_self_dmg/heroine
    #         heroine_society += i.society_dmg_weight_avg
    #         heroine_society_avg = heroine_society/heroine
    #     else:
    #         heroine += 0

    # for i in result:
    #     if i.id_drug == 3:
    #         cocaine += 1
    #         cocaine_self_dmg += i.self_dmg_weight_avg
    #         cocaine_self_avg = cocaine_self_dmg/cocaine
    #         cocaine_society += i.society_dmg_weight_avg
    #         cocaine_society_avg = cocaine_society/cocaine
    #     else:
    #         cocaine += 0
    # for i in result:
    #     if i.id_drug == 4:
    #         meta += 1
    #         meta_self_dmg += i.self_dmg_weight_avg
    #         meta_self_avg = meta_self_dmg/meta
    #         meta_society += i.society_dmg_weight_avg
    #         meta_society_avg = meta_society/meta
    #     else:
    #         meta += 0
    # for i in result:
    #     if i.id_drug == 5:
    #         tobacco += 1
    #         tobacco_self_dmg += i.self_dmg_weight_avg
    #         tobacco_self_avg = tobacco_self_dmg/tobacco
    #         tobacco_society += i.society_dmg_weight_avg
    #         tobacco_society_avg = tobacco_society/tobacco

    #     else:
    #         tobacco += 0
    # for i in result:
    #     if i.id_drug == 6:
    #         amfa += 1
    #         amfa_self_dmg += i.self_dmg_weight_avg
    #         amfa_self_avg = amfa_self_dmg/amfa
    #         amfa_society += i.society_dmg_weight_avg
    #         amfa_society_avg = amfa_society/amfa
    #     else:
    #         amfa += 0
    # for i in result:
    #     if i.id_drug == 7:
    #         marihuana += 1
    #         marihuana_self_dmg += i.self_dmg_weight_avg
    #         marihuana_self_avg = marihuana_self_dmg/marihuana
    #         marihuana_society += i.society_dmg_weight_avg
    #         marihuana_society_avg = marihuana_society/marihuana
    #     else:
    #         marihuana += 0
    # for i in result:
    #     if i.id_drug == 8:
    #         mdma += 1
    #         mdma_self_dmg += i.self_dmg_weight_avg
    #         mdma_self_avg = mdma_self_dmg/mdma
    #         mdma_society += i.society_dmg_weight_avg
    #         mdma_society_avg = mdma_society/mdma
    #     else:
    #         mdma += 0
    # for i in result:
    #     if i.id_drug == 9:
    #         mefedron += 1
    #         mefedron_self_dmg += i.self_dmg_weight_avg
    #         mefedron_self_avg = mefedron_self_dmg/mefedron
    #         mefedron_society += i.society_dmg_weight_avg
    #         mefedron_society_avg = mefedron_society/mefedron
    #     else:
    #         mefedron += 0
    # for i in result:
    #     if i.id_drug == 10:
    #         lsd += 1
    #         lsd_self_dmg += i.self_dmg_weight_avg
    #         lsd_self_avg = lsd_self_dmg/lsd
    #         lsd_society += i.society_dmg_weight_avg
    #         lsd_society_avg = lsd_society/lsd
    #     else:
    #         lsd += 0
    # for i in result:
    #     if i.id_drug == 11:
    #         psylocibine += 1
    #         psylocibine_self_dmg += i.self_dmg_weight_avg
    #         psylocibine_self_avg = psylocibine_self_dmg/psylocibine
    #         psylocibine_society += i.society_dmg_weight_avg
    #         psylocibine_society_avg = psylocibine_society/psylocibine
    #     else:
    #         psylocibine += 0
    # for i in result:
    #     if i.id_drug == 12:
    #         ketamine += 1
    #         ketamine_self_dmg += i.self_dmg_weight_avg
    #         ketamine_self_avg = ketamine_self_dmg/ketamine
    #         ketamine_society += i.society_dmg_weight_avg
    #         ketamine_society_avg = ketamine_society/ketamine
    #     else:
    #         ketamine += 0
    # for i in result:
    #     if i.id_drug == 13:
    #         dxm += 1
    #         dxm_self_dmg += i.self_dmg_weight_avg
    #         dxm_self_avg = dxm_self_dmg/dxm
    #         dxm_society += i.society_dmg_weight_avg
    #         dxm_society_avg = dxm_society/dxm
    #     else:
    #         dxm += 0
    # for i in result:
    #     if i.id_drug == 14:
    #         dmt += 1
    #         dmt_self_dmg += i.self_dmg_weight_avg
    #         dmt_self_avg = dmt_self_dmg/dmt
    #         dmt_society += i.society_dmg_weight_avg
    #         dmt_society_avg = dmt_society/dmt
    #     else:
    #         dmt += 0



    # return render_template('Result.html',
    #                        result =result, alcohol = alcohol,
    #                        cocaine = cocaine, heroine = heroine,
    #                        meta = meta, tobacco = tobacco,
    #                        amfa = amfa, marihuana = marihuana,
    #                        mdma = mdma, mefedron = mefedron,
    #                        lsd = lsd, psylocibine = psylocibine,
    #                        ketamine = ketamine, dxm = dxm, dmt = dmt,
    #                        alcohol_self_avg = alcohol_self_avg, alcohol_society_avg = alcohol_society_avg,
    #                        heroine_self_avg = heroine_self_avg, heroine_society_avg = heroine_society_avg,
    #                        cocaine_self_avg = cocaine_self_avg, cocaine_society_avg = cocaine_society_avg,
    #                        meta_self_avg = meta_self_avg, meta_society_avg = meta_society_avg,
    #                        tobacco_self_avg = tobacco_self_avg, tobacco_society_avg = tobacco_society_avg,
    #                        amfa_self_avg = amfa_self_avg, amfa_society_avg = amfa_society_avg,
    #                        marihuana_self_avg = marihuana_self_avg, marihuana_society_avg = marihuana_society_avg,
    #                        mdma_self_avg = mdma_self_avg, mdma_society_avg = mdma_society_avg,
    #                        mefedron_self_avg = mefedron_self_avg, mefedron_society_avg = mefedron_society_avg,
    #                        lsd_self_avg = lsd_self_avg, lsd_society_avg = lsd_society_avg,
    #                        psylocibine_self_avg = psylocibine_self_avg, psylocibine_society_avg = psylocibine_society_avg,
    #                        ketamine_self_avg = ketamine_self_avg, ketamine_society_avg = ketamine_society_avg,
    #                        dxm_self_avg = dxm_self_avg, dxm_society_avg = dxm_society_avg,
    #                        dmt_self_avg = dmt_self_avg, dmt_society_avg = dmt_society_avg
    #                        )



