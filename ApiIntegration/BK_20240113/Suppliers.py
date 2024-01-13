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
    url = baseURL+"suppliers"#?filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Purchase Order API to Suppliers
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Suppliers:
    supplier_id: str
    name: str
    code: str
    contact_name: str
    phone: str
    email: str
    cc_emails: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

cursor.execute("truncate table Suppliers")
page = 1
while True:
    params = {'page': page, 'per_page': 50}
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
            Suppliers.supplier_id = item["id"]
            Suppliers.name = item["name"]
            Suppliers.code = item["code"]
            Suppliers.contact_name = item["contact_name"]
            Suppliers.phone = item["phone"]
            Suppliers.email = item["email"]
            Suppliers.cc_emails = item["cc_emails"]
            Suppliers.created_at = item["created_at"]
            Suppliers.updated_at = item["updated_at"]
            Suppliers.deleted_at = item["deleted_at"]

            tuple_data_details = ( 
                                    Suppliers.supplier_id 
                                    ,Suppliers.name
                                    ,Suppliers.code 
                                    ,Suppliers.contact_name 
                                    ,Suppliers.phone
                                    ,Suppliers.email 
                                    ,Suppliers.cc_emails 
                                    ,Suppliers.created_at 
                                    ,Suppliers.updated_at 
                                    ,Suppliers.deleted_at 
                                )
            rows.append(tuple_data_details)
    except:
        pass
    
    #print(rows)
    try:
        cursor.executemany("insert into Suppliers (  \
                                    Suppliers.supplier_id \
                                    ,Suppliers.name\
                                    ,Suppliers.code \
                                    ,Suppliers.contact_name \
                                    ,Suppliers.phone\
                                    ,Suppliers.email \
                                    ,Suppliers.cc_emails \
                                    ,Suppliers.created_at \
                                    ,Suppliers.updated_at \
                                    ,Suppliers.deleted_at ) \
                        values(:1, :2, :3, :4, :5, :6, :7, \
                        TO_DATE(:8,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:9,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:10,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    
    page +=1
 