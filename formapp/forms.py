from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets, SelectField, IntegerField


class MultiCheckboxField(SelectMultipleField):
    '''
    Ta klasa dziedziczy po klasie SelectMultipleField, widgety pobrano po to,
    aby zamiast listy rozwijanej była lista z zaznaczaniem wieleokrotnego wyboru.
    Powoduje to zmiane czysto estetyczną, nic więcej.
    '''
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()



class AddUserForm(FlaskForm):
    '''Klasa odpowiedzialna za utworzenie formularza dodawania użytkownika,
    jej pola to:
    -sex -określa płeć, ma formę listy rozwijanej z dwiema opcjami, lista jednokrotnego wyboru
    -city - pole tektowe do którego ma być wpisywana nazwa miejscowości
    -age - pole numeryczne do którego zapisywany jest wiek
    -drugs -zmodyfikowana lista rozwijana wielokrotnego wyboru, tak, że wygląda jak odpowiedź wielokrotnego wyboru'''
    sex = SelectField('Płeć:',choices=[('m','Mężczyzna'),('k','Kobieta')])
    city = StringField('City:')
    age = IntegerField('age :')
    '''opcje do tego pola formularza zaciągane są z bazy danych'''
    drugs = MultiCheckboxField('Drugs', coerce=int)

    submit = SubmitField('Dalej')



