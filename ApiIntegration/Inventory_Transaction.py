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
    url = baseURL+"inventory_transactions"
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Purchase Order API to Inventory Transaction
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class InvTran:
    inventory_transaction_id: str
    branch_id: str
    branch_name: str
    other_branch_id: str
    other_branch_name: str
    supplier_id: str
    supplier_name: str
    order_id: str
    order_type: str
    creator_id: str
    creator_name: str
    poster_id: str
    poster_name: str
    purchase_order_id: str
    transfer_order_id: str
    other_transaction_id: str
    reason_id: str
    item_id: str
    item_name: str
    item_quantity: float
    item_cost: float
    item_unit: str
    item_unit_to_storage_factor: float
    item_quantity_received: float
    business_date: datetime
    reference: str
    type: int
    status: int
    paid_tax: float
    additional_cost: float
    notes: str
    invoice_number: str
    invoice_date: datetime
    created_at: datetime
    updated_at: datetime
    posted_at: datetime

cursor.execute("truncate table INVENTORY_TRANSACTION")
page = 1

while True:
    params = {'page': page, 'per_page': 50}

    current_attempt_m = 0 #current attempt on master api
    max_attempts_m = 5
    while current_attempt_m < max_attempts_m:
        try:
            response = requests.request("GET", url, headers=headers, data=payload, params=params)
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
    for m_item in responseDataMaster["data"]:
        InvTran.inventory_transaction_id = m_item["id"]
        print(InvTran.inventory_transaction_id)
        InvTran.business_date = m_item["business_date"]
        InvTran.reference = m_item["reference"]
        InvTran.type = m_item["type"]
        InvTran.status = m_item["status"]        
        InvTran.paid_tax = m_item["paid_tax"]
        InvTran.additional_cost = m_item["additional_cost"]
        InvTran.notes = m_item["notes"]
        InvTran.invoice_number = m_item["invoice_number"]
        InvTran.invoice_date = m_item["invoice_date"]
        InvTran.created_at = m_item["created_at"]
        InvTran.updated_at = m_item["updated_at"]
        InvTran.posted_at = m_item["posted_at"]
            
        current_attempt_d = 0
        max_attempts_d = 5
        while current_attempt_d<max_attempts_d:
            try:
                response = requests.request("GET", url+"/"+m_item["id"], headers=headers, data=payload)
                if response.status_code==200:
                    current_attempt_d = max_attempts_d
                    responseDataDetails=response.json()
            except:
                time.sleep(60)
                current_attempt_d +=1

        try:
            for d_item in responseDataDetails["data"]["items"]:
                try:
                    if responseDataDetails["data"]["purchase_order"] == None:
                        InvTran.purchase_order_id = ''
                    else:
                        InvTran.purchase_order_id = responseDataDetails["data"]["purchase_order"]["id"]
                    
                    if responseDataDetails["data"]["transfer_order"] == None:
                        InvTran.transfer_order_id = ''
                    else:
                        InvTran.transfer_order_id = responseDataDetails["data"]["transfer_order"]["id"]

                    if d_item["id"] != None:
                        InvTran.item_id = d_item["id"]
                    else:
                        InvTran.item_id = ''

                    if d_item["name"] != None:
                        InvTran.item_name = d_item["name"]
                    else:
                        InvTran.item_name = ''

                    if d_item["pivot"]["quantity"] != None:
                        InvTran.item_quantity = d_item["pivot"]["quantity"]
                    else:
                        InvTran.item_quantity = 0

                    if d_item["pivot"]["cost"] != None:
                        InvTran.item_cost  = d_item["pivot"]["cost"]
                    else:
                        InvTran.item_cost = 0
                    
                    if responseDataDetails["data"]["order"] != None:
                        InvTran.order_id = responseDataDetails["data"]["order"]["id"]
                        InvTran.order_type = str(responseDataDetails["data"]["order"]["type"])
                    else:
                        InvTran.order_id = ''
                        InvTran.order_type = ''

                    if responseDataDetails["data"]["supplier"] != None:
                        InvTran.supplier_id  = responseDataDetails["data"]["supplier"]["id"]
                        InvTran.supplier_name = responseDataDetails["data"]["supplier"]["name"]
                    else: 
                        InvTran.supplier_id = ''
                        InvTran.supplier_name = ''

                    if responseDataDetails["data"]["branch"] != None:
                        InvTran.branch_id = responseDataDetails["data"]["branch"]["id"]
                        InvTran.branch_name = responseDataDetails["data"]["branch"]["name"]
                    else:
                        InvTran.branch_id = ''
                        InvTran.branch_name = ''

                    if responseDataDetails["data"]["other_branch"] != None:
                        InvTran.other_branch_id = responseDataDetails["data"]["other_branch"]["id"]
                        InvTran.other_branch_name = responseDataDetails["data"]["other_branch"]["name"]
                    else:
                        InvTran.other_branch_id = ''
                        InvTran.other_branch_name = ''   

                    if responseDataDetails["data"]["creator"] != None:
                        InvTran.creator_id = responseDataDetails["data"]["creator"]["id"]
                        InvTran.creator_name = responseDataDetails["data"]["creator"]["name"]
                    else:
                        InvTran.creator_id = ''
                        InvTran.creator_name = ''

                    if responseDataDetails["data"]["poster"] != None:
                        InvTran.poster_id = responseDataDetails["data"]["poster"]["id"]
                        InvTran.poster_name  = responseDataDetails["data"]["poster"]["name"]
                    else:
                        InvTran.poster_id = ''
                        InvTran.poster_name = ''

                    #print('page: '+ str(page))
                    tuple_data_details = (InvTran.inventory_transaction_id, InvTran.business_date, InvTran.reference, InvTran.type, 
                                          InvTran.status , InvTran.paid_tax, InvTran.additional_cost, InvTran.notes, 
                                          InvTran.invoice_number, InvTran.invoice_date, InvTran.created_at, InvTran.updated_at, InvTran.posted_at,
                                          InvTran.purchase_order_id, InvTran.item_id, InvTran.item_name, InvTran.item_quantity, InvTran.item_cost,
                                          InvTran.supplier_id, InvTran.supplier_name, InvTran.branch_id, InvTran.branch_name,
                                          InvTran.creator_id, InvTran.creator_name, InvTran.poster_id, InvTran.poster_name,
                                          InvTran.order_id, InvTran.order_type, InvTran.other_branch_id, InvTran.other_branch_name,
                                          InvTran.transfer_order_id
                                          
                                          )
                    details_rows.append(tuple_data_details)
                except:
                    pass
        except KeyError:
            pass
    #print(details_rows)
    try:
        cursor.executemany("insert into INVENTORY_TRANSACTION (inventory_transaction_id, business_date, reference, type, \
                        status, paid_tax, additional_cost, notes, invoice_number, invoice_date, created_at, updated_at, posted_at,\
                        purchase_order_id, item_id, item_name, item_quantity, item_cost, supplier_id, supplier_name,\
                        branch_id, branch_name, creator_id, creator_name, poster_id, poster_name,\
                        order_id, order_type, other_branch_id, other_branch_name, transfer_order_id ) \
                        values(:1, TO_DATE(:2,'YYYY-MM-DD'), :3, :4, :5, :6, :7, :8, :9, TO_DATE(:10,'YYYY-MM-DD'), \
                       TO_DATE(:11,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:12,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:13,'YYYY-MM-DD HH24:MI:SS'),\
                       :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, :30, :31)", details_rows)
        connection.commit()
    except:
        pass

    page += 1
 
        

