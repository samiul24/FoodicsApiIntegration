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
    url = baseURL+"charges"#?filter[created_on]="+previous_date
    print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Charges Order API to Charges
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Charges:
    charge_id: str
    name: str
    name_localized: str
    type: str
    is_auto_applied: str
    order_types: str
    value: float
    is_open_charge: str
    is_calculated_using_subtotal: str
    associate_to_all_branches: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

cursor.execute("truncate table Charges")
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
            Charges.charge_id = item["id"]
            Charges.name = item["name"]
            Charges.name_localized = item["name_localized"]
            Charges.type = item["type"]
            Charges.is_auto_applied = item["is_auto_applied"]
            Charges.order_types = str(item["order_types"]).replace('[','').replace(']','')
            Charges.value = item["value"]
            Charges.is_open_charge = item["is_open_charge"]
            Charges.is_calculated_using_subtotal = item["is_calculated_using_subtotal"]
            Charges.associate_to_all_branches = item["associate_to_all_branches"]
            Charges.created_at = item["created_at"]
            Charges.updated_at = item["updated_at"]
            Charges.deleted_at = item["deleted_at"]

            tuple_data_details = (
                                     Charges.charge_id
                                    ,Charges.name 
                                    ,Charges.name_localized 
                                    ,Charges.type 
                                    ,Charges.is_auto_applied 
                                    ,Charges.order_types 
                                    ,Charges.value 
                                    ,Charges.is_open_charge 
                                    ,Charges.is_calculated_using_subtotal 
                                    ,Charges.associate_to_all_branches 
                                    ,Charges.created_at 
                                    ,Charges.updated_at 
                                    ,Charges.deleted_at 
                                )
            rows.append(tuple_data_details)
    except:
        pass
    
    print(rows)
    try:
        cursor.executemany("insert into Charges ( Charges.charge_id\
                                                ,Charges.name \
                                                ,Charges.name_localized \
                                                ,Charges.type \
                                                ,Charges.is_auto_applied \
                                                ,Charges.order_types \
                                                ,Charges.value \
                                                ,Charges.is_open_charge \
                                                ,Charges.is_calculated_using_subtotal \
                                                ,Charges.associate_to_all_branches \
                                                ,Charges.created_at \
                                                ,Charges.updated_at \
                                                ,Charges.deleted_at ) \
                        values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, \
                        TO_DATE(:11,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:12,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:13,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    
    page +=1
 
        

