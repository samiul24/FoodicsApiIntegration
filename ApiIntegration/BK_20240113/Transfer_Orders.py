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
    url = baseURL+"transfer_orders"
    url_ext = baseURL+"transfer_orders?filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Purchase Order API to Transfer_Orders
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Transfer_Orders:
    transfer_order_id: str
    business_date: datetime
    reference: str
    status: int
    notes: str
    decline_reason: str
    created_at: datetime
    updated_at: datetime
    item_id: str
    item_name: str
    item_quantity: float
    item_cost: float
    item_sku: str
    item_storage_unit: str 
    item_ingredient_unit: str
    item_costing_method: int
    branch_id: str
    branch_name: str
    warehouse_id: str
    warehouse_name: str    
    creator_id: str
    creator_name: str
    poster_id: str
    poster_name: str

#cursor.execute("truncate table Transfer_Orders")
page = 1
while True:
    params = {'page': page, 'per_page': 500}

    current_attempt_m = 0 #current attempt on master api
    max_attempts_m = 5
    while current_attempt_m < max_attempts_m:
        try:
            response = requests.request("GET", url_ext, headers=headers, data=payload, params=params)
            if response.status_code==200:
                current_attempt_m = max_attempts_m
                responseDataMaster=response.json()

        except:
            time.sleep(60)
            current_attempt_m +=1
            
    objects = responseDataMaster["data"]
    if len(objects)==0:
        exit()

    master_rows = []
    details_rows = []
    for item in responseDataMaster["data"]:
        Transfer_Orders.transfer_order_id = item["id"]
        Transfer_Orders.business_date = item["business_date"]
        Transfer_Orders.reference = item["reference"]
        Transfer_Orders.status = item["status"]
        Transfer_Orders.notes = item["notes"]
        Transfer_Orders.decline_reason = item["decline_reason"]        
        Transfer_Orders.created_at = item["created_at"]
        Transfer_Orders.updated_at = item["updated_at"]


        current_attempt_d = 0
        max_attempts_d = 5
        while current_attempt_d<max_attempts_d:
            try:
                response = requests.request("GET", url+"/"+item["id"], headers=headers, data=payload)
                if response.status_code==200:
                    current_attempt_d = max_attempts_d
                    responseDataDetails=response.json()
            except:
                time.sleep(60)
                current_attempt_d +=1

        try:
            for item in responseDataDetails["data"]["items"]:
                try:
                    Transfer_Orders.item_id = item["id"]
                    Transfer_Orders.item_name = item["name"]
                    Transfer_Orders.item_quantity = item["pivot"]["quantity"]
                    Transfer_Orders.item_sku = item["sku"]
                    Transfer_Orders.item_cost = item["cost"]
                    Transfer_Orders.item_storage_unit =  item["storage_unit"]
                    Transfer_Orders.item_ingredient_unit = item["ingredient_unit"]
                    Transfer_Orders.item_costing_method = item["costing_method"]
                    Transfer_Orders.branch_id = responseDataDetails["data"]["branch"]["id"]
                    Transfer_Orders.branch_name = responseDataDetails["data"]["branch"]["name"]
                    Transfer_Orders.warehouse_id = responseDataDetails["data"]["warehouse"]["id"]
                    Transfer_Orders.warehouse_name = responseDataDetails["data"]["warehouse"]["name"]                    
                    Transfer_Orders.creator_id = responseDataDetails["data"]["creator"]["id"]
                    Transfer_Orders.creator_name = responseDataDetails["data"]["creator"]["name"]
                    Transfer_Orders.poster_id = responseDataDetails["data"]["poster"]["id"]
                    Transfer_Orders.poster_name = responseDataDetails["data"]["poster"]["name"]
                    
                    tuple_data_details = (Transfer_Orders.transfer_order_id, Transfer_Orders.business_date, Transfer_Orders.reference,\
                                          Transfer_Orders.status, Transfer_Orders.notes, Transfer_Orders.decline_reason, Transfer_Orders.created_at, Transfer_Orders.updated_at,\
                                          Transfer_Orders.item_id, Transfer_Orders.item_name, Transfer_Orders.item_quantity, Transfer_Orders.item_sku, Transfer_Orders.item_cost,\
                                          Transfer_Orders.item_storage_unit, Transfer_Orders.item_ingredient_unit, Transfer_Orders.item_costing_method, Transfer_Orders.branch_id,\
                                          Transfer_Orders.branch_name, Transfer_Orders.warehouse_id, Transfer_Orders.warehouse_name, Transfer_Orders.creator_id, Transfer_Orders.creator_name,\
                                          Transfer_Orders.poster_id, Transfer_Orders.poster_name
                                          )
                    details_rows.append(tuple_data_details)
                except:
                    pass
        except KeyError:
            pass
    #print(details_rows)
    try:
        cursor.executemany("insert into Transfer_Orders (transfer_order_id, business_date, reference, \
                       status, notes, decline_reason, created_at, updated_at,\
                       item_id, item_name, item_quantity, item_sku, item_cost, item_storage_unit, item_ingredient_unit,\
                       item_costing_method, branch_id, branch_name, warehouse_id, warehouse_name, creator_id, creator_name,\
                       poster_id, poster_name) \
                    values(:1, TO_DATE(:2,'YYYY-MM-DD'), :3, :4, :5, :6,\
                       TO_DATE(:7,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:8,'YYYY-MM-DD HH24:MI:SS'), :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24)", details_rows)    
        connection.commit()
    except:
        pass

    page += 1

 
        

