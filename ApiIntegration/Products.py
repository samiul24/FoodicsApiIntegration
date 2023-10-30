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
    url = baseURL+"products?include=discounts,timed_events,category,tax_group,tags,groups,branches,modifiers"#?filter[created_on]="+previous_date
    print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Purchase Order API to Products
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Products:
    product_id: str
    sku: str
    name: str
    name_localized: str
    description: str
    description_localized: str
    is_active: str
    is_stock_product: str
    is_ready: str
    pricing_method: float
    selling_method: float
    costing_method: float
    price : float
    cost : float
    calories: float
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    category_id: str
    category_name : str
    discount_id: str
    timed_event_id: str
    tax_group_id: str
    tag_id: str
    group_id: str
    group_name : str
    branch_id: str
    modifier_id: str
    modifier_name: str

cursor.execute("truncate table Products")
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
        except:
            time.sleep(60)
            current_attempt_m +=1

    objects = responseData["data"]
    if len(objects)==0:
        print(1)
        exit()
        
    rows = []

    for item in responseData["data"]:
        Products.product_id = item["id"]
        Products.sku = item["sku"]
        Products.name = item["name"]
        Products.name_localized = item["name_localized"]
        Products.description = item["description"]
        Products.description_localized = item["description_localized"]
        Products.is_active = item["is_active"]
        Products.is_stock_product = item["is_stock_product"]
        Products.is_ready = item["is_ready"]
        Products.pricing_method = item["pricing_method"]
        Products.selling_method = item["selling_method"]
        Products.costing_method = item["costing_method"]
        Products.price = item["price"]
        Products.cost = item["cost"]
        Products.calories = item["calories"]
        Products.created_at = item["created_at"]
        Products.updated_at = item["updated_at"]

        if item["category"]!=None and len(item["category"])>0:
            Products.category_id = item["category"]["id"]
            Products.category_name = item["category"]["name"]
        else:
            Products.category_id = ''
            Products.category_name = ''

        if item["branches"]!=None and len(item["branches"])>0:
            for branch in item["branches"]:
                Products.branch_id = branch["id"]
        else:
            Products.branch_id = ''        

        if item["groups"]!=None and len(item["groups"])>0:
            for group in item["groups"]:
                Products.group_id = group["id"]
                Products.group_name = group["id"]
        else:
            Products.group_id = ''
            Products.group_name = ''

        if item["modifiers"]!=None and len(item["modifiers"])>0:
            for modifier in item["modifiers"]:
                Products.modifier_id = modifier["id"]
                Products.modifier_name = modifier["id"]
        else:
            Products.modifier_id = ''
            Products.modifier_name = ''
        

        tuple_data_details = (Products.product_id , Products.sku , Products.name , Products.name_localized , 
                        Products.description , Products.description_localized , Products.is_active , Products.is_stock_product,
                        Products.is_ready, Products.pricing_method, Products.selling_method, Products.costing_method,
                        Products.price, Products.cost, Products.calories, Products.created_at, 
                        Products.updated_at, Products.category_id, Products.category_name, 
                        Products.group_id, Products.group_name, Products.modifier_id, Products.modifier_name
                        )
        rows.append(tuple_data_details)

    #print(rows)
    cursor.executemany("insert into Products (Products.product_id , Products.sku , Products.name , Products.name_localized , \
                        Products.description , Products.description_localized , Products.is_active , Products.is_stock_product, \
                        Products.is_ready, Products.pricing_method, Products.selling_method, Products.costing_method, \
                        Products.price, Products.cost, Products.calories, Products.created_at, \
                        Products.updated_at, Products.category_id, Products.category_name,\
                        Products.group_id, Products.group_name, Products.modifier_id, Products.modifier_name) \
                        values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15,\
                       TO_DATE(:16,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:17,'YYYY-MM-DD HH24:MI:SS'),\
                       :18, :19, :20, :21, :22, :23)", rows)
    connection.commit()

    page += 1
 
        

