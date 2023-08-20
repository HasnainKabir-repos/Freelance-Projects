from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired
from derivbot import Account
import asyncio
import threading
from functions import get_balance

app = Flask(__name__)
app.config['SECRET_KEY'] = "nibirkabir"

apps = []

class LoginForm(FlaskForm):
    api_key = StringField(validators=[InputRequired()], 
                          render_kw={"placeholder" : "Enter API Token"})
    app_id = IntegerField(validators=[InputRequired()],
                          render_kw={"placeholder": "Enter APP ID"})

    submit = SubmitField("Save Information", render_kw={"class": "save-btn"})

def add_or_update_account(account):
    for existing_account in apps:
        if existing_account.api_token == account.api_token and existing_account.app_id == account.app_id:
            if existing_account.status:
                existing_account.status = account.status
            return

    apps.append(account)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        account = Account(api_token=form.api_key.data, app_id=form.app_id.data)
        thread = threading.Thread(target=asyncio.run, args=(account.do_authorization(),))
        thread.start()
        thread.join()
        add_or_update_account(account)

        return render_template('login.html', form=form, hide_loading_overlay=True, show_true_modal=True)

    return render_template('login.html', form=form)

@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html', accounts=apps)

@app.route('/balance')
def balance():
    mt5_list = []
    balance_thread = threading.Thread(target=lambda: mt5_list.extend(get_balance(apps=apps)))
    balance_thread.start()
    return render_template('balance.html', mt5_list=mt5_list)

if __name__ == "__main__":
    app.run(debug=True)