import json
class MessageHandler:
    def __init__(self, message, account):
        self.message = message
        self.account = account
        self.flag = False

    def handle_message(self):
        try:
            message_data = json.loads(self.message)
            
            if message_data["msg_type"] == "authorize":
                self.account.handle_authorize(message_data)

            elif message_data["msg_type"] == "mt5_login_list":
                self.account.handle_mt5(message_data)
                self.flag = True
                print(f"Succesfully fetched MT5 data")
        except Exception as e:
            print(f'Error handling messages {e}')

