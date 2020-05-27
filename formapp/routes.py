from formapp import app, db
from formapp.user_database import User, SpecificDrug, Drug
from flask import render_template, request, redirect


# Tutaj też trzeba (chyba) umieścić ewntualne funkcje POST itd.

@app.route('/') # ten fragment przekierowuje do formularza HTML
def hello_world():
    print("Poszło") # info o odpaleniu stronki
    db.create_all()  # utworzenie bazy danych z tabelami określonymi powyżej
    has_children = User.selected_drugs.any()
    q = db.session.query(User, has_children)
    for parent, has_children in q.all():
        print(parent, has_children)
    return render_template('welcome.html')


@app.route('/firstForm') # wyświetlenie pierwszego formularza
def show_firstForm():
    return render_template('firstForm.html')


@app.route("/saveFirst", methods=['POST']) # zapisywanie tego co zostało wklepane do formularza (odpala akcję /save w formularzu)
def save_first_form():
    age = request.form['age']
    user = User("M", age, "Karakan")
    selected_drugs_list = request.form
    print(selected_drugs_list)
    db.session.add(user) # testowe dodatnie do bazy danych rekordu
    db.session.commit()
    return render_template('drugForm.html')


@app.route('/drugForm') # wyświetlenie drugiego formularza formularza
def show_drugtForm():
    return render_template('frugForm.html')

@app.route('/saveDrug')
def save_drug_form():
    return redirect('/')
