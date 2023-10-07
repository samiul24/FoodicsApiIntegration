import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json
from dataclasses import dataclass
import datetime
import time


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
    url = baseURL+"inventory_item_categories"
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Purchase Order API to Inventory_Categories
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Inventory_Categories:
    id: str
    name: str
    name_localized: str
    reference: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

cursor.execute("truncate table Inventory_Categories")
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
            Inventory_Categories.id = item["id"]
            Inventory_Categories.name = item["name"]
            Inventory_Categories.name_localized = item["name_localized"]
            Inventory_Categories.reference = item["reference"]
            Inventory_Categories.created_at = item["created_at"]
            Inventory_Categories.updated_at = item["updated_at"]
            Inventory_Categories.deleted_at = item["deleted_at"]

            tuple_data_details = (Inventory_Categories.id, Inventory_Categories.name, Inventory_Categories.name_localized, 
                                Inventory_Categories.reference, Inventory_Categories.created_at, Inventory_Categories.updated_at, 
                                Inventory_Categories.deleted_at
                                )
            rows.append(tuple_data_details)
    except:
        pass
    
    #print(rows)
    try:
        cursor.executemany("insert into Inventory_Categories (id, name, name_localized, reference, \
                                                          created_at, updated_at, deleted_at) \
                        values(:1, :2, :3, :4, \
                        TO_DATE(:5,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:6,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:7,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    
    page +=1
 
        

