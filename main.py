import requests
import json
from bitcoin import * 

#https://chain.so/api/v2/address/BTC/1Lg2Qkr4g6NnGYmUiqZ2LX55gCQ3FrXBQQ
apiurl = 'https://chain.so/api/v2/address/BTC/'

def balance_check_zero(final_bal): 
  if final_bal == float(0.00000000):
    print('True') #Nachází se Nula (mělo by zahodit) DEBUG
    return True
  else: 
    print('False') #Nachází se větší zůstatek než nula DEBUG
    return False

i=0
while i == 0:
  my_private_key = random_key()
  public_key = privtopub(my_private_key)
  wallet_address = pubtoaddr(public_key)
  response = requests.get(apiurl + wallet_address)

  json_data_load = json.loads(response.text)
  print(json_data_load)
  print(json_data_load['status'], json_data_load['code'])

  final_bal = float(json_data_load["data"]["balance"]) + float(json_data_load["data"]['received_value']) + float(json_data_load["data"]['pending_value'])
  if balance_check_zero(final_bal) == True:
    print('0Bal.')
  else:
    print('---Něco nalezeno---')
    file1 = open("keys.txt","a") 
    file1.write("PK:"+ str(my_private_key) + str(response.content) + " \n")
    file1.close()
