
from deriv_api import DerivAPI


class Account:
    def __init__(self, api_token, app_id):
        self.api_token = api_token
        self.app_id = app_id
        self.status = False
        self.api = None

    def change_status(self):
        self.status = True
    
    async def do_authorization(self):
        try:
            global api 
            api = DerivAPI(app_id = self.app_id)
            self.api = api
            authorize = await api.authorize(self.api_token)

            print("Authorization Successful")
            #print(authorize)
            self.status=True
        except Exception as e:
            print(f'Authorization error occurred: {e}')
        