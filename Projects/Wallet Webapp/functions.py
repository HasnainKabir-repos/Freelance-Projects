from derivbot import Account_Mt5, Mt5
import asyncio
import threading

async def fetch_balance(apps, mt5_list):
    try:
        for account in apps:
            api = account.api
            #print(api)
            response = await api.mt5_login_list()
            
            print("Mt5 data fetched successfully")
            
            for i in response:
                mt5 = Mt5(i['email'], i['login'], i['balance'], account.wallet)
                account_mt5 = Account_Mt5(account, mt5)
                
                if account_mt5 not in mt5_list:
                    mt5_list.append(account_mt5)
    except Exception as e:
        print(f'Error fetching MT5 data: {e}')

def get_balance(apps):
    mt5_list = []

    thread = threading.Thread(target=asyncio.run, args=(fetch_balance(apps=apps, mt5_list=mt5_list),))
    thread.start()
    
    return mt5_list
