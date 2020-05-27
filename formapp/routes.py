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
    return redirect('/drugForm')


@app.route('/drugForm') # wyświetlenie drugiego formularza formularza
def show_drugtForm():
    return render_template('drugForm.html')


@app.route('/saveDrug', methods=['POST'])
def save_drug_form():
    print("Selected values list:", request.form)
    print("Example for 'damage':", request.form['damage'])
    print("It's type is:", type(int(request.form['damage'])))
    damage = int(request.form['damage'])
    f_damage = int(request.form['f_damage'])
    temp_drug_id = 1
    last_user_record = db.session.query(User).order_by(User.id.desc()).first()
    temp_user_id = last_user_record.id
    print("Last user ID:", temp_user_id)
    drug = Drug(temp_drug_id, temp_user_id, damage, f_damage)
    db.session.add(drug)
    db.session.commit()
    return redirect('/')
