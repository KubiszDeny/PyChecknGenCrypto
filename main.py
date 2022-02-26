import requests
import json
from bitcoin import * 
import time

#https://chain.so/api/v2/address/BTC/1Lg2Qkr4g6NnGYmUiqZ2LX55gCQ3FrXBQQ
apiurl = 'https://chain.so/api/v2/address/BTC/'
#Hodnota json 
#{'status': 'success', 'data': {'network': 'BTC', 'address': '1Aa5rHnRKYopi8HbkJJuYmjDm5s8f2knB4', 'balance': '0.00000000', 'received_value': '0.00000000', 'pending_value': '0.00000000', 'total_txs': 0, 'txs': []}, 'code': 200, 'message': ''}

def balance_check_zero(final_bal): 
  if final_bal == float(0.00000000):
    #print('True') #Nachází se Nula (mělo by zahodit) DEBUG
    return True
  else: 
    #print('False') #Nachází se větší zůstatek než nula DEBUG
    return False


i=0
while i == 0:
  my_private_key = random_key()
  public_key = privtopub(my_private_key)
  wallet_address = pubtoaddr(public_key)
  response = requests.get(apiurl + wallet_address)
  #print(response.text) #Debug
  if "We're sorry, but something went wrong" in response.text: #Pokud API selže json_data_load upadnou na chybu - We're sorry, but something went wrong. viz. wrong.html
    print('Něco je špatně, ') #DEBUG
    data_to_write_err = str(time.ctime()),'PK:', str(my_private_key),' WalletAddr.: ',str(wallet_address),'\n', str(response.content) + "\n\n\n"
    file1 = open("errlog.txt","a") 
    file1.write(str(data_to_write_err))
    file1.close()
    time.sleep(10)
    continue
  else:
    json_data_load = json.loads(response.text)
    #  print(json_data_load)
    print('Status API', json_data_load['code'],'-', json_data_load['status'],'; Adresa:', json_data_load["data"]['address'], ' Typ:', json_data_load["data"]['network'])

    final_bal = float(json_data_load["data"]["balance"]) + float(json_data_load["data"]['received_value']) + float(json_data_load["data"]['pending_value'])
    if balance_check_zero(final_bal) == True:
        print('Zero Balance:', float(final_bal))
    else:
        print('---Něco nalezeno---')
        file1 = open("keys.txt","a")
        data_to_write_found = str(time.ctime()),'PK:', str(my_private_key),' WalletAddr.: ',str(wallet_address),'\n', " \n\n\n"
        file1.write(str(data_to_write_found))
        file1.close()
