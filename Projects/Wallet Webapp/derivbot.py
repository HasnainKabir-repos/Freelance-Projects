from deriv_api import DerivAPI

class Account:
    def __init__(self, api_token, app_id):
        self.api_token = api_token
        self.app_id = app_id
        self.wallet = 0
        self.status = False
        self.api = None

    def change_status(self):
        self.status = True
    
    async def do_authorization(self):
        try:
            self.api = DerivAPI(app_id = self.app_id)

            authorize = await self.api.authorize(self.api_token)
            print("Authorization Successful")
            
            self.wallet = authorize["authorize"]['balance']
            self.change_status()
        except Exception as e:
            print(f'Authorization error occurred: {e}')

class Mt5:
    def __init__(self, email, loginid, balance, wallet):
        self.email = email
        self.loginid = loginid
        self.balance = balance
        self.wallet = wallet


class Account_Mt5:
    def __init__(self, account, mt5):
        self.account = account
        self.mt5 = mt5


