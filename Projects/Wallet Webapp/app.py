from flask import Flask, render_template,  request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired
from derivbot import Account, Transfer
import threading
from functools import wraps
import websocket
import json
from flask_socketio import SocketIO
from MessageHandler import MessageHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = "nibirkabir"
socketio = SocketIO(app)

apps = []
execution_flag = threading.Event()
transfer_flag = threading.Event()

def socket_connect(account):
    ws_url = f"wss://frontend.binaryws.com/websockets/v3?l=EN&app_id={account.app_id}"
    
    def on_open(ws):
        print('[open] Connection established')
        print('Sending to server')
        send_message = json.dumps({"ping": 1})
        ws.send(send_message)
        account.setConnection(ws)
        account.do_authorization()
        add_or_update_account(account=account)
        
    def on_message(ws, message):
        global data_received
        print(f"[message] Data received from server: {message}")
        account.setConnection(ws)
        # Handle received message here

        handler = MessageHandler(message=message, account=account)
        handler.handle_message()
        global msg 

        if handler.flag:
            execution_flag.set()
        if handler.transfer_status:
            msg = json.loads(handler.message)
            transfer_flag.set()

    def on_close(ws, close_status_code, close_msg):
        if close_status_code == 1000:
            print(f"[close] Connection closed cleanly, code={close_status_code} reason={close_msg}")
        else:
            print("[close] Connection died")
        
    def on_error(ws, error):
        print(f"[error] {error}")

    ws = websocket.WebSocketApp(ws_url, 
                                on_open=on_open, 
                                on_message=on_message, 
                                on_close=on_close, 
                                on_error=on_error,
                                )
    ws.run_forever(reconnect=5)

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
        socket_thread = threading.Thread(target=socket_connect, args=(account, ))
        socket_thread.start()

        return render_template('login.html', form=form, hide_loading_overlay=True, show_true_modal=True)

    return render_template('login.html', form=form)

@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html', accounts=apps)

def prepare_mt5_data(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        for i in apps:
            i.get_mt5_list()
            execution_flag.wait()
            for j in i.mt5_list:
                j.total = i.total
        return route_function(*args, **kwargs)
    return decorated_function

@app.route('/balance')
@prepare_mt5_data
def balance():
    mt5_lst = []
    for i in apps:
       mt5_lst.extend(i.mt5_list)

    return render_template('balance.html', mt5_list=mt5_lst, loader=False)

def process_users():
    usernames = []
    for i in apps:
        for j in i.mt5_list:
            if j.email not in usernames:
                usernames.append(j.email)
    return usernames

def process_options(username):
    options=[]
    for i in apps:
        for j in i.mt5_list:
            if j.email == username:
                options.append(j.loginid)
    return options

@app.route('/transfer')
def transfer():
    balance()
    usernames = process_users()
    options = []
    if len(usernames) > 0:
        options = process_options(usernames[0])
    return render_template('transfer.html', options=options, usernames=usernames)

@app.route('/change_mt5_accounts', methods=['POST'])
def change_mt5_accounts():
    user = request.form.get('user')
    options = process_options(user)
    return jsonify({'options': options})

@app.route('/process_transfer', methods=['POST'])
def process_transfer():
    username = request.form.get('user');
    account_from = request.form.get('account_from')
    amount = int(request.form.get('amount'))
    account_to = request.form.get('account_to')

    transfer = Transfer(username, account_from, account_to, amount)
    transfer.transfer(apps)
    transfer_flag.wait()

    if msg and msg['error']:
        err = msg['error']['message']
        return jsonify({"message": err})
    else:
        return jsonify({"message":"Transferred Funds Successfully"})

if __name__ == "__main__":
    app.run(debug=True)