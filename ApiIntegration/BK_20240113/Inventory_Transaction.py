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
    #url = baseURL+"inventory_transactions"
    url =     baseURL+"inventory_transactions?include=branch,other_branch,order,purchase_order,transfer_order,items,supplier,creator,poster"#&filter[created_on]="+previous_date
    url_ext = baseURL+"inventory_transactions?include=branch,other_branch,order,purchase_order,transfer_order,items,supplier,creator,poster"#&filter[created_on]="+previous_date
    url_sup = baseURL+"suppliers"
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
    supplier_code: str
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
cursor.execute("insert into Run_Log(API_Name) values('Inventory_Transaction')")

page = 1
row_cnt = 0
while True:
    param = {'page': page, 'per_page': 1000000}

    current_attempt_m = 0 #current attempt on master api
    max_attempts_m = 50

    while current_attempt_m < max_attempts_m:
        #print('Number of attempt: ' + str(current_attempt_m))
        response = requests.request("GET", url_ext, headers=headers, data=payload, params=param)
        if response.status_code==200:
            current_attempt_m = max_attempts_m
            responseDataMaster=response.json()

        else:
            #print('Exception')
            time.sleep(60)
            current_attempt_m +=1

    objects = responseDataMaster["data"]
    if len(objects)==0:
        #cursor.execute("UPDATE Run_Log SET End_Time = SYSTIMESTAMP, Total_Record_Count= "+str(row_cnt)+" WHERE API_Name = 'Inventory_Transaction'  AND TRUNC(Start_Time) = TRUNC(SYSDATE)")
        #connection.commit()
        exit()
        
    master_rows = []
    details_rows = []
    for m_item in responseDataMaster["data"]:
        InvTran.inventory_transaction_id = m_item["id"]
        #print(InvTran.inventory_transaction_id)
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

        if m_item["purchase_order"] == None:
            InvTran.purchase_order_id = ''
        else:
            InvTran.purchase_order_id = m_item["purchase_order"]["id"]
                    
        if m_item["transfer_order"] == None:
            InvTran.transfer_order_id = ''
        else:
            InvTran.transfer_order_id = m_item["transfer_order"]["id"]
        if m_item["order"] != None:
            InvTran.order_id = m_item["order"]["id"]
            InvTran.order_type = str(m_item["order"]["type"])
        else:
            InvTran.order_id = ''
            InvTran.order_type = ''

        if m_item["supplier"] != None:
            InvTran.supplier_id  = m_item["supplier"]["id"]
            InvTran.supplier_name = m_item["supplier"]["name"]
            if len(InvTran.supplier_id)>0:
                try:
                    ResSup = requests.request("GET", url_sup+"/"+InvTran.supplier_id, headers=headers, data=payload)
                    if ResSup.status_code == 200:
                        ResSupData = ResSup.json()
                        InvTran.supplier_code = ResSupData["data"]["code"]
                except:
                    InvTran.supplier_code = ''
        else: 
            InvTran.supplier_id = ''
            InvTran.supplier_name = ''
            InvTran.supplier_code = ''
        #print('Sup Id: '+InvTran.supplier_id)
        #print('Sup Code: '+InvTran.supplier_code)
        if m_item["branch"] != None:
            InvTran.branch_id = m_item["branch"]["id"]
            InvTran.branch_name = m_item["branch"]["name"]
        else:
            InvTran.branch_id = ''
            InvTran.branch_name = ''

        if m_item["other_branch"] != None:
            InvTran.other_branch_id = m_item["other_branch"]["id"]
            InvTran.other_branch_name = m_item["other_branch"]["name"]
        else:
            InvTran.other_branch_id = ''
            InvTran.other_branch_name = ''   

        if m_item["creator"] != None:
            InvTran.creator_id = m_item["creator"]["id"]
            InvTran.creator_name = m_item["creator"]["name"]
        else:
            InvTran.creator_id = ''
            InvTran.creator_name = ''

        if m_item["poster"] != None:
            InvTran.poster_id = m_item["poster"]["id"]
            InvTran.poster_name  = m_item["poster"]["name"]
        else:
            InvTran.poster_id = ''
            InvTran.poster_name = ''            

        try:
            for d_item in m_item["items"]:
                try:
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

                    #print('page: '+ str(page))
                    tuple_data_details = (InvTran.inventory_transaction_id, InvTran.business_date, InvTran.reference, InvTran.type, 
                                          InvTran.status , InvTran.paid_tax, InvTran.additional_cost, InvTran.notes, 
                                          InvTran.invoice_number, InvTran.invoice_date, InvTran.created_at, InvTran.updated_at, InvTran.posted_at,
                                          InvTran.purchase_order_id, InvTran.item_id, InvTran.item_name, InvTran.item_quantity, InvTran.item_cost,
                                          InvTran.supplier_id, InvTran.supplier_name, InvTran.branch_id, InvTran.branch_name,
                                          InvTran.creator_id, InvTran.creator_name, InvTran.poster_id, InvTran.poster_name,
                                          InvTran.order_id, InvTran.order_type, InvTran.other_branch_id, InvTran.other_branch_name,
                                          InvTran.transfer_order_id, InvTran.supplier_code
                                          
                                          )
                    details_rows.append(tuple_data_details)
                except:
                    pass
        except KeyError:
            cursor.execute("insert into Error_Log(API_Name,Error_Description) values('Inventory_Transaction','D_Item Data Processing Error')")
    #print(details_rows)
    try:
        cursor.executemany("insert into INVENTORY_TRANSACTION (inventory_transaction_id, business_date, reference, type, \
                        status, paid_tax, additional_cost, notes, invoice_number, invoice_date, created_at, updated_at, posted_at,\
                        purchase_order_id, item_id, item_name, item_quantity, item_cost, supplier_id, supplier_name,\
                        branch_id, branch_name, creator_id, creator_name, poster_id, poster_name,\
                        order_id, order_type, other_branch_id, other_branch_name, transfer_order_id, supplier_code ) \
                        values(:1, TO_DATE(:2,'YYYY-MM-DD'), :3, :4, :5, :6, :7, :8, :9, TO_DATE(:10,'YYYY-MM-DD'), \
                       TO_DATE(:11,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:12,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:13,'YYYY-MM-DD HH24:MI:SS'),\
                       :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, :30, :31, :32)", details_rows)
        connection.commit()
    except:
        cursor.execute("insert into Error_Log(API_Name,Error_Description) values('Inventory_Transaction','Records Insertion Error')")

    page += 1
