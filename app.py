

from flask import Flask, render_template, request
from flask_wtf import FlaskForm

app = Flask(__name__)


@app.route('/')  # http://127.0.0.1:5000/
def home_page():
    return render_template('home_page.html')


@app.route('/sig_form')
def sig_form():
    return render_template('sig_form.html')


@app.route('/fuck_you')
def fuck_you():
    login = request.args.get('login')
    is_lower = login.islower()
    is_upper = login.isupper()
    is_digit = False
    for l in login:
        if True == l.isdigit():
            is_digit = True

    if is_lower == is_upper == False and is_digit == True:
        return render_template('fuck_you.html', login=login)
    else:
        return render_template('wrong.html', login=login)


if __name__ == '__main__':
    app.run(debug=True)
