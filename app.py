from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField, IntegerField)
from wtforms.validators import DataRequired


app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'

# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
class InfoForm(FlaskForm):
    '''
    To klasa główna prostego formularza, dziedziczy po klasie flask_wtf
    używanej do tworzenia formularzy

    W tym prostym formularzu żeby go zatwierdzić i przejść do kolejnej strony,
    wszystkie dane musza być wypełnione poprawnie
    '''

    sex = StringField('Podaj płeć?',validators=[DataRequired()])
    age = IntegerField('podaj wiek')
    did_you_take_drugs  = BooleanField("czy ćpałeś?")
    test = RadioField('jaki miałeś wtedy nastrój:', choices=[('mood_one','Happy'),('mood_two','Excited')])
    drugslist = SelectField('jakie narkotyki brałeś:',
                          choices=[('he', 'hera'), ('ko', 'koka'),
                                   ('ha', 'hash')])
    feedback = TextAreaField()
    submit = SubmitField('Submit')



@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = InfoForm()
    # If the form is valid on submission (we'll talk about validation next)
    '''
    Ten if sprawdza, czy naciśnięto przycisk tatwierdzający wypełnienie ankiety
    jeśli nie widzimy strone główną, przekazaliśmy do niej kalse form, dzięki temu 
    możemy wyświetlać jej pola przez plik html
    Po wypełnienu prawidłowym wszystkich pól, przekierowywuje nas na strone podsumowującą
    '''
    if form.validate_on_submit():
        # Grab the data from the breed on the form.

        session['sex'] = form.sex.data
        session['age'] = form.age.data
        session['did_you_take_drugs'] = form.did_you_take_drugs.data
        session['test'] = form.test.data
        session['drugslist'] = form.drugslist.data
        session['feedback'] = form.feedback.data

        return redirect(url_for("thank_you"))


    return render_template('main_page.html', form=form)


@app.route('/than_kyou')
def thank_you():

    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(debug=True)
