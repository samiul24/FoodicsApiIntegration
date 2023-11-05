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
    url = baseURL+"house_account_transactions?include=user,order,customer"#&filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from House_Account_Transactions API to House_Account_Transactions
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class House_Account_Transactions:
    house_account_transaction_id: str
    amount: float
    old_balance: float
    new_balance: float
    notes: str
    user_id: str
    customer_id: str
    order_id: str
    created_at: datetime
    updated_at: datetime

#cursor.execute("truncate table House_Account_Transactions")
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
            House_Account_Transactions.house_account_transaction_id = item["id"]
            House_Account_Transactions.amount = item["amount"]
            House_Account_Transactions.old_balance = item["old_balance"]
            House_Account_Transactions.new_balance = item["new_balance"]
            House_Account_Transactions.notes = item["notes"]
            House_Account_Transactions.user_id = item["user"]["id"]
            House_Account_Transactions.customer_id = item["customer"]["id"]
            House_Account_Transactions.order_id = item["order"]["id"]
            House_Account_Transactions.created_at = item["id"]
            House_Account_Transactions.updated_at = item["id"]
            

            tuple_data_details = ( 
                                    House_Account_Transactions.house_account_transaction_id,
                                    House_Account_Transactions.amount,
                                    House_Account_Transactions.old_balance,
                                    House_Account_Transactions.new_balance,
                                    House_Account_Transactions.notes,
                                    House_Account_Transactions.user_id,
                                    House_Account_Transactions.customer_id,
                                    House_Account_Transactions.order_id,
                                    House_Account_Transactions.created_at,
                                    House_Account_Transactions.updated_at,
                                )

            rows.append(tuple_data_details)
    except:
        pass

    try:
        cursor.executemany("insert into House_Account_Transactions ( \
                                                                        House_Account_Transactions.house_account_transaction_id,\
                                                                        House_Account_Transactions.amount,\
                                                                        House_Account_Transactions.old_balance,\
                                                                        House_Account_Transactions.new_balance,\
                                                                        House_Account_Transactions.notes,\
                                                                        House_Account_Transactions.user_id,\
                                                                        House_Account_Transactions.customer_id,\
                                                                        House_Account_Transactions.order_id,\
                                                                        House_Account_Transactions.created_at,\
                                                                        House_Account_Transactions.updated_at \
                                                                    ) \
                        values(:1, :2, :3, :4, :5, :6, :7, :8, \
                        TO_DATE(:9,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:10,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    page += 1
 
        

