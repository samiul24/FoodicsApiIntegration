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
#print(previous_date)

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
    url = baseURL+"purchase_orders?include=items, supplier,submitter,branch,creator,poster"#&filter[created_on]="+previous_date
    url_ext = baseURL+"purchase_orders?include=items, supplier,submitter,branch,creator,poster"#&filter[created_on]="+previous_date
    #print(url)
    
    Authorization = os.environ.get("Authorization")
    #exit()
except:
    pass

#data load from List Purchase Order API to Purchase_Orders
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Purchase_Orders:
    purchase_order_id: str
    business_date: datetime
    delivery_date: datetime
    reference: str
    additional_cost: float
    status: int
    notes: str
    item_id: str
    item_name: str
    item_quantity: float
    item_cost: float
    item_unit: str
    item_unit_to_storage_factor: float
    item_quantity_received: float
    item_sku: str
    item_storage_unit: str 
    item_ingredient_unit: str
    supplier_id: str
    supplier_name: str
    submitter_id: str
    submitter_name: str
    branch_id: str
    branch_name: str
    creator_id: str
    creator_name: str
    poster_id: str
    poster_name: str
    created_at: datetime
    updated_at: datetime
    reviewed_at: datetime
    closed_at: datetime
    submitted_at: datetime


cursor.execute("truncate table Purchase_Orders")
page = 1
while True:
    #print('page')
    param = {'page': page, 'per_page': 100000}

    current_attempt_m = 0 #current attempt on master api
    max_attempts_m = 5000

    while current_attempt_m < max_attempts_m:
        #print('Number of attempt: ' + str(current_attempt_m))
        response = requests.request("GET", url_ext, headers=headers, data=payload, params=param)
        #print(response)
        
        if response.status_code==200:
            #print('Status code: '+ str(response.status_code))
            current_attempt_m = max_attempts_m
            responseDataMaster=response.json()
        else:
            #print('Exception')
            time.sleep(60)
            current_attempt_m +=1
            
    objects = responseDataMaster["data"]
    if len(objects)==0:
        exit()

    master_rows = []
    details_rows = []
    for item in responseDataMaster["data"]:
        #print(item)
        Purchase_Orders.purchase_order_id = item["id"]
        Purchase_Orders.business_date = item["business_date"]
        Purchase_Orders.delivery_date = item["delivery_date"]
        Purchase_Orders.reference = item["reference"]
        #print(Purchase_Orders.reference)
        Purchase_Orders.additional_cost = item["additional_cost"]
        Purchase_Orders.status = item["status"]
        Purchase_Orders.notes = item["notes"]
        Purchase_Orders.created_at = item["created_at"]
        Purchase_Orders.updated_at = item["updated_at"]
        Purchase_Orders.reviewed_at = item["reviewed_at"]
        Purchase_Orders.closed_at = item["closed_at"]
        Purchase_Orders.submitted_at = item["submitted_at"]

        Purchase_Orders.supplier_id = item["supplier"]["id"]
        Purchase_Orders.supplier_name = item["supplier"]["name"]

        try:
            Purchase_Orders.submitter_id = item["submitter"]["id"]
            Purchase_Orders.submitter_name = item["submitter"]["name"]
        except:
            Purchase_Orders.submitter_id = ''
            Purchase_Orders.submitter_name = ''
        
        Purchase_Orders.branch_id = item["branch"]["id"]
        Purchase_Orders.branch_name = item["branch"]["name"]
        
        Purchase_Orders.creator_id = item["creator"]["id"]
        Purchase_Orders.creator_name = item["creator"]["name"]

        try:
            Purchase_Orders.poster_id = item["poster"]["id"]
            Purchase_Orders.poster_name = item["poster"]["name"]
        except:
            Purchase_Orders.poster_id = ''
            Purchase_Orders.poster_name = ''        

        for item in item["items"]:
            try:
                #print(item)
                Purchase_Orders.item_id = item["id"]
                #print(Purchase_Orders.item_id)
                Purchase_Orders.item_name = item["name"]
                Purchase_Orders.item_quantity = item["pivot"]["quantity"]
                Purchase_Orders.item_cost = item["pivot"]["cost"]
                Purchase_Orders.item_unit = item["pivot"]["unit"]
                Purchase_Orders.item_unit_to_storage_factor = item["pivot"]["unit_to_storage_factor"]
                Purchase_Orders.item_quantity_received = item["pivot"]["quantity_received"]
                Purchase_Orders.item_sku = item["sku"]
                
                Purchase_Orders.item_storage_unit =  item["storage_unit"]
                Purchase_Orders.item_ingredient_unit = item["ingredient_unit"]

                    
                tuple_data_details = (Purchase_Orders.purchase_order_id, Purchase_Orders.business_date, Purchase_Orders.delivery_date, Purchase_Orders.reference, 
                        Purchase_Orders.additional_cost, Purchase_Orders.status, Purchase_Orders.notes, Purchase_Orders.created_at,
                        Purchase_Orders.updated_at, Purchase_Orders.reviewed_at, Purchase_Orders.closed_at, Purchase_Orders.submitted_at, 
                        Purchase_Orders.item_id, Purchase_Orders.item_name, Purchase_Orders.item_quantity,Purchase_Orders.item_cost,
                        Purchase_Orders.item_unit, Purchase_Orders.item_unit_to_storage_factor,Purchase_Orders.item_quantity_received, 
                        Purchase_Orders.item_sku, Purchase_Orders.item_storage_unit, Purchase_Orders.item_ingredient_unit,
                        Purchase_Orders.supplier_id, Purchase_Orders.supplier_name, Purchase_Orders.branch_id, Purchase_Orders.branch_name,
                        Purchase_Orders.submitter_id, Purchase_Orders.submitter_name, Purchase_Orders.creator_id, Purchase_Orders.creator_name,
                        Purchase_Orders.poster_id, Purchase_Orders.poster_name
                        )

                details_rows.append(tuple_data_details)
            except:
                pass


    #print(details_rows)
    try:
        cursor.executemany("insert into Purchase_Orders (purchase_order_id, business_date, delivery_date, \
                                    reference, additional_cost, status, notes, \
                                    created_at, updated_at, reviewed_at, closed_at, submitted_at, item_id, item_name, item_quantity, \
                                    item_cost, item_unit, item_unit_to_storage_factor, item_quantity_received, item_sku,\
                                    item_storage_unit, item_ingredient_unit, supplier_id, supplier_name, branch_id, branch_name,\
                                    submitter_id, submitter_name, creator_id, creator_name, poster_id, poster_name) \
                        values(:1, TO_DATE(:2,'YYYY-MM-DD'), TO_DATE(:3,'YYYY-MM-DD'), :4, :5, :6, :7, \
                        TO_DATE(:8,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:9,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:10,'YYYY-MM-DD HH24:MI:SS'),\
                        TO_DATE(:11,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:12,'YYYY-MM-DD HH24:MI:SS'), :13, :14, \
                        :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, :30, :31, :32)", details_rows)
        connection.commit()
    except:
        pass

    page += 1
 
    

