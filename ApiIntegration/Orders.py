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
    url = baseURL+"orders?include=branch,promotion,customer,customer_address,charges,payments,products,combos"
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
class Orders:
    order_id: str
    promotion_id: str
    discount_type: int
    reference: str
    type: str
    source: str
    status: str
    delivery_status: str
    guests: str
    kitchen_notes: str
    customer_notes: str
    business_date: datetime
    subtotal_price: float
    discount_amount: float
    rounding_amount: float
    total_price: float
    tax_exclusive_discount_amount: float
    delay_in_seconds: float
    opened_at: datetime
    accepted_at: datetime
    due_at: datetime
    driver_assigned_at: datetime
    dispatched_at: datetime
    driver_collected_at: datetime
    delivered_at: datetime
    closed_at: datetime
    created_at: datetime
    updated_at: datetime
    check_number: str

    branch_id: str
    branch_name: str
    customer_id: str
    customer_name: str
    product_id: str
    product_discount_type: str
    product_quantity: float
    product_returned_quantity: float
    product_unit_price: float
    product_discount_amount: float
    product_total_price: float
    product_total_cost: float
    product_tax_exclusive_discount_amount: float
    product_tax_exclusive_unit_price: float
    product_tax_exclusive_total_price: float

cursor.execute("truncate table Orders")
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

    for item in responseData["data"]:
        print(1)
        Orders.order_id = item["id"]
        Orders.promotion_id = item["promotion_id"]         
        Orders.discount_type = str(item["discount_type"])
        Orders.reference = item["reference"]            
        Orders.type = str(item["type"])
        Orders.source = str(item["source"])           
        Orders.status = str(item["status"])
        Orders.delivery_status = str(item["delivery_status"])          
        Orders.guests = str(item["guests"])
        Orders.kitchen_notes = item["kitchen_notes"]
        Orders.customer_notes = item["customer_notes"]             
        Orders.subtotal_price = item["subtotal_price"]
        Orders.discount_amount = item["discount_amount"]                  
        Orders.rounding_amount = item["rounding_amount"]
        Orders.total_price = item["total_price"]
        Orders.tax_exclusive_discount_amount = item["tax_exclusive_discount_amount"]
        Orders.delay_in_seconds = item["delay_in_seconds"]
        Orders.check_number = item["check_number"]
        Orders.opened_at = item["opened_at"]
        Orders.accepted_at = item["accepted_at"]
        Orders.due_at = item["due_at"]
        Orders.driver_assigned_at = item["driver_assigned_at"]
        Orders.dispatched_at = item["dispatched_at"]
        Orders.driver_collected_at = item["driver_collected_at"]
        Orders.delivered_at = item["delivered_at"]
        Orders.closed_at = item["closed_at"]
        Orders.created_at = item["created_at"]
        Orders.updated_at = item["updated_at"]

        Orders.branch_id = item["branch"]["id"]
        Orders.branch_name = item["branch"]["name"]

        if item["customer"]!=None:
            Orders.customer_id = item["customer"]["id"]
            Orders.customer_name = item["customer"]["name"]
        else:
            Orders.customer_id = ''
            Orders.customer_name = ''

        if item["products"]!=None:
            for product in item["products"]:
                Orders.product_id = product["id"]
                Orders.product_discount_type = str(product["discount_type"])
                Orders.product_quantity = product["quantity"]
                Orders.product_returned_quantity = product["returned_quantity"]
                Orders.product_unit_price = product["unit_price"]
                Orders.product_discount_amount = product["discount_amount"]
                Orders.product_total_price = product["total_price"]
                Orders.product_total_cost = product["total_cost"]
                Orders.product_tax_exclusive_discount_amount = product["tax_exclusive_discount_amount"]
                Orders.product_tax_exclusive_unit_price = product["tax_exclusive_unit_price"]
                Orders.product_tax_exclusive_total_price = product["tax_exclusive_total_price"]

                tuple_data_details = (Orders.order_id , Orders.promotion_id , Orders.discount_type , Orders.reference , 
                        Orders.type , Orders.source , Orders.status , Orders.delivery_status , Orders.guests , Orders.kitchen_notes , Orders.customer_notes , 
                        Orders.subtotal_price , Orders.discount_amount , Orders.rounding_amount , Orders.total_price , Orders.tax_exclusive_discount_amount, 
                        Orders.delay_in_seconds , Orders.check_number, Orders.opened_at , Orders.accepted_at,  Orders.due_at , Orders.driver_assigned_at, Orders.dispatched_at,
                        Orders.driver_collected_at, Orders.delivered_at , Orders.closed_at , Orders.created_at , Orders.updated_at,
                        Orders.branch_id , Orders.branch_name, Orders.customer_id, Orders.customer_name,
                        Orders.product_id, Orders.product_discount_type, Orders.product_quantity, Orders.product_returned_quantity,
                        Orders.product_unit_price, Orders.product_discount_amount, Orders.product_total_price, Orders.product_total_cost,
                        Orders.product_tax_exclusive_discount_amount, Orders.product_tax_exclusive_unit_price,
                        Orders.product_tax_exclusive_total_price
                        )
                rows.append(tuple_data_details)

        else:
            Orders.product_id = ''
            Orders.product_discount_type = '0'
            Orders.product_quantity = 0
            Orders.product_returned_quantity = 0
            Orders.product_unit_price = 0
            Orders.product_discount_amount = 0
            Orders.product_total_price = 0
            Orders.product_total_cost = 0
            Orders.product_tax_exclusive_discount_amount = 0
            Orders.product_tax_exclusive_unit_price = 0
            Orders.product_tax_exclusive_total_price = 0


    #print(rows)
    cursor.executemany("insert into Orders (Orders.order_id , Orders.promotion_id , Orders.discount_type , Orders.reference , \
                        Orders.type , Orders.source , Orders.status , Orders.delivery_status , Orders.guests , Orders.kitchen_notes , Orders.customer_notes , \
                        Orders.subtotal_price , Orders.discount_amount , Orders.rounding_amount , Orders.total_price , Orders.tax_exclusive_discount_amount, \
                        Orders.delay_in_seconds , Orders.check_number, Orders.opened_at , Orders.accepted_at,  Orders.due_at , Orders.driver_assigned_at, Orders.dispatched_at, \
                        Orders.driver_collected_at, Orders.delivered_at , Orders.closed_at , Orders.created_at , Orders.updated_at, \
                        Orders.branch_id , Orders.branch_name, Orders.customer_id, Orders.customer_name,\
                        Orders.product_id, Orders.product_discount_type, Orders.product_quantity, Orders.product_returned_quantity, \
                        Orders.product_unit_price, Orders.product_discount_amount, Orders.product_total_price, Orders.product_total_cost,\
                        Orders.product_tax_exclusive_discount_amount, Orders.product_tax_exclusive_unit_price,\
                        Orders.product_tax_exclusive_total_price ) \
                        values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, \
                        TO_DATE(:19,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:20,'YYYY-MM-DD HH24:MI:SS') , TO_DATE(:21,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:22,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:23,'YYYY-MM-DD HH24:MI:SS'),\
                        TO_DATE(:24,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:25,'YYYY-MM-DD HH24:MI:SS') , TO_DATE(:26,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:27,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:28,'YYYY-MM-DD HH24:MI:SS'), \
                        :29, :30, :31, :32, :33, :34, :35, :36, :37, :38, :39, :40, :41, :42, :43)", rows)
    connection.commit()

    page += 1
 
        

