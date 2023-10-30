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
    url = baseURL+"customers"#&filter[created_on]="+previous_date
    print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Customers API to Customers
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Customers:
    house_account_balance: str
    loyalty_balance: str
    customer_id: str
    name: str
    dial_code: str
    phone: str
    email: str
    gender: str
    birth_date: datetime
    is_blacklisted: str
    is_house_account_enabled: str
    house_account_limit: str
    is_loyalty_enabled: str
    order_count: str
    last_order_at: datetime
    notes: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

cursor.execute("truncate table Customers")
page = 1
while True:
    params = {'page': page, 'per_page': 500}
    #print(page)
    current_attempt_m = 0 #current attempt on master api
    max_attempts_m = 5
    while current_attempt_m < max_attempts_m:
        try:
            response = requests.request("GET", url, headers=headers, data=payload, params=params)
            if response.status_code==200:
                current_attempt_m = max_attempts_m
                responseData=response.json()
        except:
            time.sleep(60)
            current_attempt_m +=1

    objects = responseData["data"]
    if len(objects)==0:
        exit()
        
    rows = []
    try:
        for item in responseData["data"]:
            Customers.house_account_balance  = item["house_account_balance"]
            Customers.loyalty_balance  = item["loyalty_balance"]
            Customers.customer_id  = item["id"]
            Customers.name  = item["name"]
            Customers.dial_code  = item["dial_code"]
            Customers.phone  = item["phone"]
            Customers.email  = item["email"]
            Customers.gender  = item["gender"]
            Customers.birth_date  = item["birth_date"]
            Customers.is_blacklisted  = item["is_blacklisted"]
            Customers.is_house_account_enabled  = item["is_house_account_enabled"]
            Customers.house_account_limit  = item["house_account_limit"]
            Customers.is_loyalty_enabled  = item["is_loyalty_enabled"]
            Customers.order_count = item["order_count"]
            Customers.last_order_at = item["last_order_at"]
            Customers.notes  = item["notes"]
            Customers.created_at  = item["created_at"]
            Customers.updated_at = item["updated_at"]
            Customers.deleted_at = item["deleted_at"]

            tuple_data_details = (
                                        Customers.house_account_balance , 
                                        Customers.loyalty_balance , 
                                        Customers.customer_id , 
                                        Customers.name , 
                                        Customers.dial_code , 
                                        Customers.phone , 
                                        Customers.email , 
                                        Customers.gender , 
                                        Customers.is_blacklisted , 
                                        Customers.is_house_account_enabled , 
                                        Customers.house_account_limit , 
                                        Customers.is_loyalty_enabled , 
                                        Customers.order_count ,
                                        Customers.notes , 
                                        Customers.last_order_at ,
                                        Customers.birth_date , 
                                        Customers.created_at ,
                                        Customers.updated_at ,
                                        Customers.deleted_at                                      
                                                        )
            rows.append(tuple_data_details)
    except:
        pass
    
    #print(rows)
    try:
        cursor.executemany("insert into Customers ( \
                                            Customers.house_account_balance , \
                                            Customers.loyalty_balance , \
                                            Customers.customer_id , \
                                            Customers.name , \
                                            Customers.dial_code , \
                                            Customers.phone , \
                                            Customers.email , \
                                            Customers.gender , \
                                            Customers.is_blacklisted , \
                                            Customers.is_house_account_enabled , \
                                            Customers.house_account_limit , \
                                            Customers.is_loyalty_enabled , \
                                            Customers.order_count ,\
                                            Customers.last_order_at ,\
                                            Customers.notes , \
                                            Customers.birth_date , \
                                            Customers.created_at ,\
                                            Customers.updated_at ,\
                                            Customers.deleted_at  ) \
                            values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, TO_DATE(:15,'YYYY-MM-DD HH24:MI:SS'),\
                            TO_DATE(:16,'YYYY-MM-DD'), TO_DATE(:17,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:18,'YYYY-MM-DD HH24:MI:SS'),\
                            TO_DATE(:19,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass

    
    page +=1
 
        

