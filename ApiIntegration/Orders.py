import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json
from dataclasses import dataclass
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
    url = baseURL+"orders?include=branch,promotion,customer,customer_address,charges,payments,payments.payment_method,products.product,combos"#&filter[created_on]="+previous_date
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

    payment_id: str
    payment_amount: float
    payment_tendered: float
    payment_tips: float
    payment_method_id: str
    payment_method_name: str
    payment_method_type: str

    combos_id: str
    combos_discount_type: str
    combos_discount_amount: float
    combos_quantity: float
    charges_charge_id: str
    charges_charge_name: str
    charges_tax_id: str
    charges_tax_name: str

cursor.execute("truncate table Orders")
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
        Orders.business_date = item["business_date"]         
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

        if item["payments"]!=None:
            for payment in item["payments"]:
                Orders.payment_id = payment["id"]
                Orders.payment_amount = payment["amount"]
                Orders.payment_tendered = payment["tendered"]
                Orders.payment_tips = payment["tips"]
                Orders.payment_method_id = payment["payment_method"]["id"]
                Orders.payment_method_name = payment["payment_method"]["name"]
                Orders.payment_method_type = payment["payment_method"]["type"]
        else:
            Orders.payment_id = ''
            Orders.payment_amount = 0
            Orders.payment_tendered = 0
            Orders.payment_tips = 0
            Orders.payment_method_id = ''
            Orders.payment_method_name = ''
            Orders.payment_method_type = ''

        
        if item["combos"]!=None and len(item["combos"])>0:
            try:
                for combo in item["combos"]:
                    Orders.combos_id = combo["id"]
                    Orders.combos_discount_type = combo["discount_type"]
                    Orders.combos_discount_amount = combo["discount_amount"]
                    Orders.combos_quantity = combo["quantity"]
            except:
                Orders.combos_id = ''
                Orders.combos_discount_type = ''
                Orders.combos_discount_amount = 0
                Orders.combos_quantity = 0
        else:
            Orders.combos_id = ''
            Orders.combos_discount_type = ''
            Orders.combos_discount_amount = 0
            Orders.combos_quantity = 0

        if item["charges"]!=None and len(item["charges"])>0:
            try:
                for charge in item["charges"]:
                    if charge["charge"]!=None and len(charge["charge"])>0:
                        Orders.charges_charge_id = charge["charge"]["id"]
                        Orders.charges_charge_name = charge["charge"]["name"]
                    else:
                        Orders.charges_charge_id = ''
                        Orders.charges_charge_name = ''

                    if charge["taxes"]!=None and len(charge["taxes"])>0:
                        for tax in charge["taxes"]:
                            Orders.charges_tax_id = tax["id"]
                            Orders.charges_tax_name = tax["name"]
                    else:
                        Orders.charges_tax_id = ''
                        Orders.charges_tax_name = ''
            except:
                Orders.charges_charge_id = ''
                Orders.charges_charge_name = ''
                Orders.charges_tax_id = ''
                Orders.charges_tax_name = ''
        else:
            Orders.charges_charge_id = ''
            Orders.charges_charge_name = ''
            Orders.charges_tax_id = ''
            Orders.charges_tax_name = ''


        if item["products"]!=None and len(item["products"])>0 :
            for product in item["products"]:
                Orders.product_id = product["product"]["id"]
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
                        Orders.product_tax_exclusive_total_price,
                        Orders.payment_id, Orders.payment_amount, Orders.payment_tendered, Orders.payment_tips,
                        Orders.combos_id, Orders.combos_discount_type, Orders.combos_discount_amount, Orders.combos_quantity,
                        Orders.charges_charge_id, Orders.charges_charge_name, Orders.charges_tax_id,  Orders.charges_tax_name,
                        Orders.payment_method_id, Orders.payment_method_name, Orders.payment_method_type, Orders.business_date
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
            #print(item)
            tuple_data_details = (Orders.order_id , Orders.promotion_id , Orders.discount_type , Orders.reference , 
                        Orders.type , Orders.source , Orders.status , Orders.delivery_status , Orders.guests , Orders.kitchen_notes , Orders.customer_notes , 
                        Orders.subtotal_price , Orders.discount_amount , Orders.rounding_amount , Orders.total_price , Orders.tax_exclusive_discount_amount, 
                        Orders.delay_in_seconds , Orders.check_number, Orders.opened_at , Orders.accepted_at,  Orders.due_at , Orders.driver_assigned_at, Orders.dispatched_at,
                        Orders.driver_collected_at, Orders.delivered_at , Orders.closed_at , Orders.created_at , Orders.updated_at,
                        Orders.branch_id , Orders.branch_name, Orders.customer_id, Orders.customer_name,
                        Orders.product_id, Orders.product_discount_type, Orders.product_quantity, Orders.product_returned_quantity,
                        Orders.product_unit_price, Orders.product_discount_amount, Orders.product_total_price, Orders.product_total_cost,
                        Orders.product_tax_exclusive_discount_amount, Orders.product_tax_exclusive_unit_price,
                        Orders.product_tax_exclusive_total_price,
                        Orders.payment_id, Orders.payment_amount, Orders.payment_tendered, Orders.payment_tips,
                        Orders.combos_id, Orders.combos_discount_type, Orders.combos_discount_amount, Orders.combos_quantity,
                        Orders.charges_charge_id, Orders.charges_charge_name, Orders.charges_tax_id,  Orders.charges_tax_name,
                        Orders.payment_method_id, Orders.payment_method_name, Orders.payment_method_type,Orders.business_date
                        )
            rows.append(tuple_data_details)


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
                        Orders.product_tax_exclusive_total_price,\
                        Orders.payment_id, Orders.payment_amount, Orders.payment_tendered, Orders.payment_tips,\
                        Orders.combos_id, Orders.combos_discount_type, Orders.combos_discount_amount, Orders.combos_quantity,\
                        Orders.charges_charge_id, Orders.charges_charge_name, Orders.charges_tax_id,  Orders.charges_tax_name, \
                        Orders.payment_method_id, Orders.payment_method_name, Orders.payment_method_type, Orders.business_date ) \
                        values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, \
                        TO_DATE(:19,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:20,'YYYY-MM-DD HH24:MI:SS') , TO_DATE(:21,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:22,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:23,'YYYY-MM-DD HH24:MI:SS'),\
                        TO_DATE(:24,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:25,'YYYY-MM-DD HH24:MI:SS') , TO_DATE(:26,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:27,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:28,'YYYY-MM-DD HH24:MI:SS'), \
                        :29, :30, :31, :32, :33, :34, :35, :36, :37, :38, :39, :40, :41, :42, :43, :44, :45, :46, :47, :48, :49, :50, :51, :52, :53, :54, :55, :56, :57, :58, TO_DATE(:59,'YYYY-MM-DD HH24:MI:SS'))", rows)
    connection.commit()

    page += 1
 
        

