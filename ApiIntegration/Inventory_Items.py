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
    url = baseURL+"inventory_items"
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Purchase Order API to Inventory_Items
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Inventory_Items:
    id: str
    name: str
    name_localized: str
    sku: str
    barcode: str
    cost: float
    minimum_level: float
    maximum_level: float
    par_level: float
    storage_unit: str
    ingredient_unit: str
    storage_to_ingredient_factor: float
    costing_method: float
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    is_product: str

cursor.execute("truncate table Inventory_Items")
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
            Inventory_Items.id = item["id"]
            Inventory_Items.name = item["name"]         
            Inventory_Items.name_localized = item["name_localized"]         
            Inventory_Items.sku = item["sku"]            
            Inventory_Items.barcode = item["barcode"]
            Inventory_Items.cost = item["cost"]            
            Inventory_Items.minimum_level = item["minimum_level"]
            Inventory_Items.maximum_level = item["maximum_level"]              
            Inventory_Items.par_level = item["par_level"]
            Inventory_Items.storage_unit = item["storage_unit"]
            Inventory_Items.ingredient_unit = item["ingredient_unit"]             
            Inventory_Items.storage_to_ingredient_factor = item["storage_to_ingredient_factor"]
            Inventory_Items.costing_method = item["costing_method"]                  
            Inventory_Items.created_at = item["created_at"]
            Inventory_Items.updated_at = item["updated_at"]
            Inventory_Items.deleted_at = item["deleted_at"]
            Inventory_Items.is_product = item["is_product"]

            tuple_data_details = (Inventory_Items.id, Inventory_Items.name, Inventory_Items.name_localized, 
                                Inventory_Items.sku, Inventory_Items.barcode, Inventory_Items.cost, Inventory_Items.minimum_level,
                                Inventory_Items.maximum_level, Inventory_Items.par_level, Inventory_Items.storage_unit,
                                Inventory_Items.ingredient_unit, Inventory_Items.storage_to_ingredient_factor, 
                                Inventory_Items.costing_method, Inventory_Items.created_at, Inventory_Items.updated_at, 
                                Inventory_Items.deleted_at, Inventory_Items.is_product
                                )

            rows.append(tuple_data_details)
    except:
        pass

    try:
        cursor.executemany("insert into Inventory_Items (id, name, name_localized, sku, barcode, cost, minimum_level, maximum_level,\
                                                    par_level, storage_unit, ingredient_unit, storage_to_ingredient_factor, \
                                                    costing_method, created_at, updated_at, deleted_at, is_product) \
                        values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, \
                        TO_DATE(:14,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:15,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:16,'YYYY-MM-DD HH24:MI:SS'), :17)", rows)
        connection.commit()
    except:
        pass
    page += 1
 
        

