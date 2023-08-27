
import json
class Account:
    def __init__(self, api_token, app_id):
        self.api_token = api_token
        self.app_id = app_id
        self.wallet = 0
        self.status = False
        self.connection = None
        self.mt5_list = []
        self.total = 0

    def change_status(self):
        self.status = True
    
    def setConnection(self, connection):
        self.connection = connection

    def do_authorization(self):
        try:
            authorize = json.dumps({"authorize": self.api_token})
            self.connection.send(authorize)
            print("Authorization Successful")
        except Exception as e:
            print(f'Authorization error occurred: {e}')

    def get_mt5_list(self):
        try:
            mt5_login_list = json.dumps({"mt5_login_list": 1})
            self.connection.send(mt5_login_list)
            
        except Exception as e:
            print(f'Error fetching Mt5 data: {e}')

    def handle_authorize(self, message):
        self.wallet = message["authorize"]["balance"]
        self.change_status()

    def handle_mt5(self, message):
        try:
            self.mt5_list = []
            res = message['mt5_login_list']
            for i in res:
                mt5 = Mt5(i['email'], i['login'], i['balance'], self.wallet)
                self.mt5_list.append(mt5)

            self.calculate_total()

            print(f'MT5 data written')
        except Exception as e:
            print(f'Error adding MT5 data to list: {e}')

    def calculate_total(self):
        self.total = 0
        for i in self.mt5_list:
            self.total += i.balance
        self.total += self.wallet

class Mt5:
    def __init__(self, email, loginid, balance, wallet):
        self.email = email
        self.loginid = loginid
        self.balance = balance
        self.wallet = wallet
        self.total = 0




