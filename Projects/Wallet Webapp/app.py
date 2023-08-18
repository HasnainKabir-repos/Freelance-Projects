from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired
from derivbot import Account
import asyncio
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = "nibirkabir"

apps = []

class LoginForm(FlaskForm):
    api_key = StringField(validators=[InputRequired()], 
                          render_kw={"placeholder" : "Enter API Token"})
    app_id = IntegerField(validators=[InputRequired()],
                          render_kw={"placeholder": "Enter APP ID"})

    submit = SubmitField("Save Information", render_kw={"class": "save-btn"})

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        account = Account(api_token=form.api_key.data, app_id=form.app_id.data)
        thread = threading.Thread(target=asyncio.run, args=(account.do_authorization(),))
        thread.start()
        thread.join()
        apps.append(account)

        return render_template('login.html', form=form, hide_loading_overlay=True, show_true_modal=True)

    return render_template('login.html', form=form)

@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html')

if __name__ == "__main__":
    app.run(debug=True)