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
    url = baseURL+"gift_card_products?include=tags,category"#&filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from Gift_Card_Products API to Gift_Card_Products
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Gift_Card_Products:
    gift_card_id: str
    name: str
    name_localized: str
    sku: str
    barcode: str
    pricing_method: float
    price: float
    is_active: str
    category_id: str
    category_name: str
    category_name_localized: str
    category_reference: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

#cursor.execute("truncate table Gift_Card_Products")
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
            Gift_Card_Products.gift_card_id = item["id"]
            Gift_Card_Products.name = item["name"]
            Gift_Card_Products.name_localized = item["name_localized"]
            Gift_Card_Products.sku = item["sku"]
            Gift_Card_Products.barcode = item["barcode"]
            Gift_Card_Products.pricing_method = item["pricing_method"]
            Gift_Card_Products.price = item["price"]
            Gift_Card_Products.is_active = item["is_active"]
            Gift_Card_Products.category_id = item["category"]["id"]
            Gift_Card_Products.category_name = item["category"]["name"]
            Gift_Card_Products.category_name_localized = item["category"]["name_localized"]
            Gift_Card_Products.category_reference = item["category"]["reference"]
            Gift_Card_Products.created_at = item["created_at"]
            Gift_Card_Products.updated_at = item["updated_at"]
            Gift_Card_Products.deleted_at = item["deleted_at"]
            

            tuple_data_details = ( 
                                        Gift_Card_Products.gift_card_id 
                                        ,Gift_Card_Products.name 
                                        ,Gift_Card_Products.name_localized 
                                        ,Gift_Card_Products.sku 
                                        ,Gift_Card_Products.barcode 
                                        ,Gift_Card_Products.pricing_method 
                                        ,Gift_Card_Products.price 
                                        ,Gift_Card_Products.is_active 
                                        ,Gift_Card_Products.category_id 
                                        ,Gift_Card_Products.category_name 
                                        ,Gift_Card_Products.category_name_localized 
                                        ,Gift_Card_Products.category_reference 
                                        ,Gift_Card_Products.created_at 
                                        ,Gift_Card_Products.updated_at 
                                        ,Gift_Card_Products.deleted_at 
                                )

            rows.append(tuple_data_details)
    except:
        pass

    try:
        cursor.executemany("insert into Gift_Card_Products (     Gift_Card_Products.gift_card_id \
                                                                ,Gift_Card_Products.name \
                                                                ,Gift_Card_Products.name_localized \
                                                                ,Gift_Card_Products.sku \
                                                                ,Gift_Card_Products.barcode \
                                                                ,Gift_Card_Products.pricing_method \
                                                                ,Gift_Card_Products.price \
                                                                ,Gift_Card_Products.is_active \
                                                                ,Gift_Card_Products.category_id \
                                                                ,Gift_Card_Products.category_name \
                                                                ,Gift_Card_Products.category_name_localized \
                                                                ,Gift_Card_Products.category_reference \
                                                                ,Gift_Card_Products.created_at \
                                                                ,Gift_Card_Products.updated_at \
                                                                ,Gift_Card_Products.deleted_at ) \
                        values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, \
                        TO_DATE(:13,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:14,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:15,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    page += 1
 
        

