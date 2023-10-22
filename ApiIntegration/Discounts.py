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
    url = baseURL+"discounts?include=products,product_tags,categories,combos,branches"
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Purchase Order API to Orders
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Discounts:
    Discount_id: str
    name: str
    name_localized: str
    qualification: float
    amount: float
    minimum_product_price: float
    minimum_order_price: float
    maximum_amount: float
    is_taxable: str
    reference: str
    order_types: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    product_id: str
    product_tag_id: str
    category_id: str
    combo_id: str
    branch_id: str
    branch_name: str

cursor.execute("truncate table Discounts")
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
        exit()
        
    rows = []

    for item in responseData["data"]:
        Discounts.Discount_id = item["id"]
        Discounts.name = item["name"]
        Discounts.name_localized = item["name_localized"]
        Discounts.qualification = item["qualification"]
        Discounts.amount = item["amount"]
        Discounts.minimum_product_price = item["minimum_product_price"]
        Discounts.minimum_order_price = item["minimum_order_price"]
        Discounts.maximum_amount = item["maximum_amount"]
        Discounts.is_taxable = item["is_taxable"]
        Discounts.reference = item["reference"]
        Discounts.order_types = str(item["order_types"]).replace('[','').replace(']','')
        Discounts.created_at = item["created_at"]
        Discounts.updated_at = item["updated_at"]
        Discounts.deleted_at = item["deleted_at"]
        print(Discounts.order_types)

        if item["products"]!=None and len(item["products"])>0:
            for product in item["products"]:
                Discounts.product_id = product["id"]
        else:
            Discounts.product_id = ''
        
        if item["combos"]!=None and len(item["combos"])>0:
            try:
                for combo in item["combos"]:
                    Discounts.combo_id = combo["id"]
            except:
                Discounts.combo_id = ''
        else:
            Discounts.combo_id = ''

        if item["product_tags"]!=None and len(item["product_tags"])>0:
            try:
                for product_tag in item["product_tags"]:
                    Discounts.product_tag_id = product_tag["id"]
            except:
                Discounts.product_tag_id = ''
        else:
            Discounts.product_tag_id = ''

        if item["categories"]!=None and len(item["categories"])>0:
            try:
                for category in item["categories"]:
                    Discounts.category_id = category["id"]
            except:
                Discounts.category_id = ''
        else:
            Discounts.category_id = ''


        if item["branches"]!=None and len(item["branches"])>0 :
            for branch in item["branches"]:
                Discounts.branch_id = branch["id"]
                Discounts.branch_name = branch["name"]
              
                tuple_data_details = (Discounts.Discount_id, Discounts.name, Discounts.name_localized, Discounts.qualification, Discounts.amount,
                                      Discounts.minimum_product_price, Discounts.minimum_order_price, Discounts.maximum_amount, Discounts.is_taxable,
                                      Discounts.reference, Discounts.order_types, Discounts.created_at, Discounts.updated_at, Discounts.deleted_at,
                                      Discounts.product_id, Discounts.combo_id, Discounts.category_id, Discounts.branch_id, Discounts.branch_name)
                rows.append(tuple_data_details)


        #print(rows)
        cursor.executemany("insert into Discounts (Discounts.Discount_id, Discounts.name, Discounts.name_localized, Discounts.qualification, Discounts.amount,\
                                      Discounts.minimum_product_price, Discounts.minimum_order_price, Discounts.maximum_amount, Discounts.is_taxable,\
                                      Discounts.reference, Discounts.order_types, Discounts.created_at, Discounts.updated_at, Discounts.deleted_at,\
                                      Discounts.product_id, Discounts.combo_id, Discounts.category_id, Discounts.branch_id, Discounts.branch_name) \
                            values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, \
                            TO_DATE(:12,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:13,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:14,'YYYY-MM-DD HH24:MI:SS'),\
                           :15, :16, :17, :18, :19)", rows)
        connection.commit()

        page += 1
 
        

