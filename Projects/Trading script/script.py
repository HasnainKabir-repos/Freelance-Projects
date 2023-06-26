
import requests
import json
import xlwings as xw
import pyotp
from smartapi.smartConnect import SmartConnect
from smartapi.smartExceptions import SmartAPIException
from smartapi.smartApiWebsocket import SmartWebSocket
import time
import base64

def login(client_id, mPIN, totp, api_key):
    try:
        obj = SmartConnect(api_key=api_key)
        # Generate session
        data = obj.generateSession(client_id, mPIN, totp)
        
        if data['status'] == True:
            refreshToken = data['data']['refreshToken']
            token =obj.generateToken(refreshToken)
            feedToken = obj.getfeedToken()
            print(f'Succesfully logged in using Client ID {client_id}')
            return (refreshToken, feedToken, obj)
        else:
            msg = data['message']
            print(f'login: {msg}')
            
            return None
    
    except SmartAPIException as e:
        print('SmartAPIException occurred during login:', str(e))

    except Exception as e:
        print('An error occurred during login:', str(e))


def generateTOTP(secret_key):
    
    try:
        totp = pyotp.TOTP(secret_key)
        totp_value = totp.now()
        return totp_value
    except Exception as e:
        print('Error generating TOTP', str(e))
        return None

def generateTokens():
    excel_file = 'order.xlsm'
    sheet1_name = 'Sheet1'
    sheet2_name = 'Sheet2'

    try:
        # Open the Excel file
        wb = xw.Book(excel_file)
        sheet1 = wb.sheets[sheet1_name]
        sheet2 = wb.sheets[sheet2_name]

        last_row = sheet2.range('A' + str(sheet2.cells.last_cell.row)).end('up').row

        for row in range(2, last_row + 1):
            client_id_cell = sheet2.range('A' + str(row))
            password_cell = sheet2.range('B' + str(row))
            secret_key_cell = sheet2.range('D' + str(row))
            api_key_cell = sheet2.range('C' + str(row))
            PIN_cell = sheet2.range('E' + str(row))

            client_id = client_id_cell.value
            password = password_cell.value
            secret_key = secret_key_cell.value
            api_key = api_key_cell.value
            PIN = int(PIN_cell.value)

            if client_id and PIN and secret_key and api_key:
                TOTP_val = generateTOTP(secret_key)

                # Write the TOTP value to the Excel file
                sheet2.range('F' + str(row)).value = str(TOTP_val)

                print(f'Client ID: {client_id} PIN: {PIN} Secret Key: {secret_key} TOTP: {TOTP_val}')
                
                (refreshToken, feedToken, obj) = login(client_id, PIN, TOTP_val, api_key)
                
                if refreshToken and feedToken:
                    #print(f'{client_id}, RefreshToken: {refreshToken} FeedToken: {feedToken}')
                    
                    sheet2.range('G' + str(row)).value = str(refreshToken)
                    sheet2.range('H' + str(row)).value = str(feedToken)
                    
                    return (refreshToken, feedToken, client_id, obj)
                else:
                    print(f'Error loggin in for Client ID: {client_id}')
                    
                    return None, None, None
                
            else:
                print(f'Skipped row {row} due to missing variable')
                
                return None, None, None

        # Save the workbook
        wb.save()

    except FileNotFoundError:
        print('Excel file not found.')
    except Exception as e:
        print('An error occurred:', str(e))

empty = []
def scrape_script_details(script_name, exch_token):
    with open('angelbroking.json') as json_file:
        data = json.load(json_file)

    for item in data:
        if item['symbol'] == script_name:
            empty.append(f"{exch_token}|{item['token']}&")
            return item['exch_seg'], item['token']          

    return None, None

def fillScriptDetails():
    excel_file = "order.xlsm"
    sheet1_name = 'Sheet1'
    
    try:
        wb = xw.Book(excel_file)
        sheet = wb.sheets[sheet1_name]

        last_row = sheet.range('A' + str(sheet.cells.last_cell.row)).end('up').row

        for row in range(2, last_row + 1):
            script_cell = sheet.range('D' + str(row))
            exch_cell = sheet.range('F'+ str(row))
            code_cell = sheet.range('E' + str(row))
            exch_token = sheet.range('C' + str(row)).value

            script = script_cell.value

            if script:
                (exchange, token) = scrape_script_details(script, exch_token)

                if exchange and token:

                    try:
                        exch_cell.value = str(exchange)
                        code_cell.value = str(token)
                    except Exception as e:
                        printf(f'An error occurred when trying to fill Script Code and Exchange column {str(e)}')

                else:
                    print(f'Cannot find information about Script {script} on angelbroking.json')
            else:
                print(f'Row skipped due to missing value of Column: Script in {row}')
    
        wb.save()
    except FileNotFoundError:
        print(f'Excel file not found')
    except Exception as e:
        print(f'An error occurred {str(e)}')
        

data = {}
def generateScriptInfo(exchange, symbol, token, ltp, obj):
    if symbol not in data:
        LTP = obj.ltpData(exchange, symbol, token)
        data[symbol] = {
            "high": LTP["data"]["high"],
            "low" : LTP["data"]["low"],
            "open" : LTP["data"]["open"]
        }
        
        return symbol, LTP["data"]["high"],  LTP["data"]["low"], LTP["data"]["open"]
    
    else:
        if float(ltp) >= data[i]["high"]:
            data[i]["high"] = float(ltp)
        if float(ltp) <= data[i]["low"]:
            data[i]["low"] = float(ltp)

        return symbol, data[symbol]["high"], data[symbol]["low"], data[i]["open"]
            


def sendData(message, obj):
    
    excel_file = 'order.xlsm'
    sheet1_name = "Sheet1"
    
    try:
        wb = xw.Book(excel_file)
        sheet = wb.sheets[sheet1_name]
    
        ltp = message[0]["ltp"]
        token = message[0]["token"]

        if ltp and token:
            name, high, low, openx = generateScriptInfo(exchange, name, ltp, obj)

        last_row = sheet.range('A' + str(sheet.cells.last_cell.row)).end('up').row

        for row in range(2, last_row + 1):
            code = sheet.range('E' + str(row)).value

            if code and code == token:
                sheet.range('G' + str(row)).value = openx
                sheet.range('H' + str(row)).value = high
                sheet.range('I' + str(row)).value = low
                sheet.range('K' + str(row)).value = ltp
                
        wb.save()
        
    except Exception as e:
        print(f'An error occurred {str(e)}')   
    finally:
        check_change_and_order(obj)
    

def generateScriptData(obj):
    
    excel_file = 'order.xlsm'
    sheet1_name = "Sheet1"
    
    try:
        wb = xw.Book(excel_file)
        sheet = wb.sheets[sheet1_name]
        
        last_row = sheet.range('A' + str(sheet.cells.last_cell.row)).end('up').row
        
        for row in range(2, last_row+1):
            name = sheet.range('D' + str(row)).value
            exchange = sheet.range('F' + str(row)).value
            code = sheet.range('E' + str(row)).value
            
            if name and exchange and code:
                data = obj.ltpData(exchange, name, code)

                if data['status'] == True:

                    sheet.range('G' + str(row)).value = data['data']['open']
                    sheet.range('H' + str(row)).value = data['data']['high']
                    sheet.range('I' + str(row)).value = data['data']['low']
                    sheet.range('J' + str(row)).value = data['data']['close']
                    sheet.range('K' + str(row)).value = data['data']['ltp']

        wb.save()
        
    except Exception as e:
        print(f'An error occurred {str(e)}')

def check_change_and_order(obj):
    excel_file = "order.xlsm"
    sheet1_name = 'Sheet1'
    
    try:
        wb = xw.Book(excel_file)
        sheet = wb.sheets[sheet1_name]
        
        last_row = sheet.range('A' + str(sheet.cells.last_cell.row)).end('up').row
        
        while True:
            for row in range(2, last_row+1):
                status = sheet.range('Q' + str(row)).value

                if status == "Buying...":
                    sheet.range('P' + str(row)).value = ""
                    print(f'Buy order at row: {row}')
                    
                    if(ordermanagement('BUY', row, sheet, obj)):

                        sheet.range('Q' + str(row)).value = "Executed"
                    else:
                        sheet.range('Q' + str(row)).value = "Failed"
                        
                elif status == "Selling...":
                    sheet.range('P' + str(row)).value = ""
                    print(f'Sell order at row: {row}')
                    
                    if(ordermanagement('SELL', row, sheet, obj)):
                        
                        sheet.range('Q' + str(row)).value = "Executed"
                    else:
                        sheet.range('Q' + str(row)).value = "Failed"
                    
                    
    except Exception as e:
        print(f'An error occurred: {str(e)}')





def ordermanagement(transactionType, row, sheet, obj):
    tradingsymbol = sheet.range('D' + str(row)).value
    symboltoken = sheet.range('E' + str(row)).value
    exchange = sheet.range('F' + str(row)).value
    ordertype = sheet.range('O' + str(row)).value
    producttype = sheet.range('M' + str(row)).value
    price = sheet.range('K' + str(row)).value
    quantity = sheet.range('L' + str(row)).value
    squareoff = sheet.range('S' + str(row)).value
    stoploss = sheet.range('T' +  str(row)).value
    
    orderparams = {
        "variety" : "NORMAL",
        "tradingsymbol" : tradingsymbol,
        "symboltoken" : int(symboltoken),
        "transactiontype": transactionType,
        "exchange" : exchange,
        "ordertype" : ordertype,
        "producttype" : producttype,
        "duration" : "DAY",
        "price" : str(price),
        "squareoff" :str(squareoff),
        "stoploss" : str(stoploss),
        "quantity" : str(quantity)
    }
    
    print(orderparams)
    #time.sleep(2)
    data=obj.placeOrder(orderparams)
    
    if data['message'] == "SUCCESS":
        orderId = data["data"]["orderid"]
        print(f'{transactionType} placed for {tradingsymbol}, at {price} order id:{orderId}')
        sheet.range('R' + str(row)).value = str(orderId)
        return True
    else:
        return False




def socketOpen(task, token, feedToken, user_id, obj):
    ss = SmartWebSocket(feedToken, user_id)
    ss.HB_INTERVAL = 10

    def on_message(ws, message):
        sendData(message, obj)

    def on_open(ws):
        print("On Open")
        ss.subscribe(task, token)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("Close")

    # Assign the callbacks.
    ss._on_open = on_open
    ss._on_message = on_message
    ss._on_error = on_error
    ss._on_close = on_close

    ss.connect()




def main():

    (refreshToken, feedToken, client_id, obj) = generateTokens()
    fillScriptDetails()
    generateScriptData(obj)
    
    newS = "".join([i for i in empty])
    token = newS[:-1]
    task = "mw"
    print(token)
    socketOpen(task, token, feedToken, client_id, obj)  
    



if __name__ == '__main__':
    main()



