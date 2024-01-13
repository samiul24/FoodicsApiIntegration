import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json
from dataclasses import dataclass
import datetime
import time
from datetime import datetime, timedelta

# Get the previous date
previous_date = datetime.now().date()-timedelta(days=1)

# Format the previous date as "YYYY-MM-DD"
previous_date = previous_date.strftime('%Y-%m-%d')


#read project directory
env_path = os.path.dirname(__file__).replace('\\','/')
env_path = os.path.dirname(env_path)
sys.path.append(env_path)
from Conn.OracleConn import connect_to_oracle

#connect with oracle DB
connection = connect_to_oracle()
cursor = connection.cursor()

#baseURL & token read
try:
    baseURL = os.environ.get("baseURL")
    url = baseURL+"gift_card_transactions?include=order,gift_card&filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from Gift_Card_Transactions API to Gift_Card_Transactions
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Gift_Card_Transactions:
    gift_card_transaction_id: str
    amount: float
    old_balance: float
    new_balance: float
    gift_card_id: str
    order_id: str
    created_at: datetime

#cursor.execute("truncate table Gift_Card_Transactions")
cursor.execute("insert into Run_Log(API_Name) values('Gift_Card_Transactions')")
page = 1
while True:
    params = {'page': page, 'per_page': 5000}
    #print(page)
    current_attempt_m = 0 #current attempt on master api
    max_attempts_m = 5
    while current_attempt_m < max_attempts_m:
        try:
            response = requests.request("GET", url, headers=headers, data=payload, params=params)
            if response.status_code==200:
                current_attempt_m = max_attempts_m
                responseData=response.json()
            else:
                time.sleep(60)
                current_attempt_m +=1

        except:
            time.sleep(60)
            current_attempt_m +=1

    objects = responseData["data"]
    if len(objects)==0:
        exit()
        
    rows = []
    try:
        for item in responseData["data"]:
            Gift_Card_Transactions.gift_card_transaction_id = item["id"]
            Gift_Card_Transactions.amount = item["amount"]
            Gift_Card_Transactions.old_balance  = item["old_balance"]
            Gift_Card_Transactions.new_balance = item["new_balance"]
            Gift_Card_Transactions.gift_card_id = item["gift_card"]["id"]
            Gift_Card_Transactions.order_id = item["order"]["id"]
            Gift_Card_Transactions.created_at = item["created_at"]
            

            tuple_data_details = ( 
                                    Gift_Card_Transactions.gift_card_transaction_id,
                                    Gift_Card_Transactions.amount,
                                    Gift_Card_Transactions.old_balance,
                                    Gift_Card_Transactions.new_balance,
                                    Gift_Card_Transactions.gift_card_id,
                                    Gift_Card_Transactions.order_id,
                                    Gift_Card_Transactions.created_at
                                )

            rows.append(tuple_data_details)
    except:
        pass

    try:
        cursor.executemany("insert into Gift_Card_Transactions ( Gift_Card_Transactions.gift_card_transaction_id, \
                                                                Gift_Card_Transactions.amount, \
                                                                Gift_Card_Transactions.old_balance,\
                                                                Gift_Card_Transactions.new_balance,\
                                                                Gift_Card_Transactions.gift_card_id,\
                                                                Gift_Card_Transactions.order_id,\
                                                                Gift_Card_Transactions.created_at ) \
                        values(:1, :2, :3, :4, :5, :6, \
                        TO_DATE(:7,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    page += 1
 
        

