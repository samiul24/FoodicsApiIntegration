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
    url = baseURL+"branches?include=tax_group,products,modifier_options,combos,tags,discounts,charges"#&filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from Branches API to Branches
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Branches:
    branch_id: str
    name: str
    name_localized: str
    reference: str
    type: str
    latitude: str
    longitude: str
    created_at: str
    updated_at: datetime
    deleted_at: datetime 
    phone: str
    address: str

#cursor.execute("truncate table Branches")
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
    try:
        for item in responseData["data"]:
            Branches.branch_id = item["id"]     
            Branches.name = item["name"]       
            Branches.name_localized = item["name_localized"]                  
            Branches.reference = item["reference"]            
            Branches.type = item["type"]
            Branches.latitude = item["latitude"]            
            Branches.longitude = item["longitude"]            
            Branches.created_at = item["created_at"]
            Branches.updated_at = item["updated_at"]
            Branches.deleted_at = item["deleted_at"]
            Branches.phone = item["phone"]
            Branches.address = item["address"]            

            tuple_data_details = ( 
                                                Branches.branch_id,   
                                                Branches.name,   
                                                Branches.name_localized,                
                                                Branches.reference,          
                                                Branches.type,
                                                Branches.latitude,          
                                                Branches.longitude,           
                                                Branches.created_at,
                                                Branches.updated_at,
                                                Branches.deleted_at,
                                                Branches.phone,
                                                Branches.address, 
                                )

            rows.append(tuple_data_details)
    except:
        pass

    try:
        cursor.executemany("insert into Branches (\
                                                Branches.branch_id,\
                                                Branches.name,\
                                                Branches.name_localized,\
                                                Branches.reference,\
                                                Branches.type,\
                                                Branches.latitude,\
                                                Branches.longitude,\
                                                Branches.created_at,\
                                                Branches.updated_at,\
                                                Branches.deleted_at,\
                                                Branches.phone,\
                                                Branches.address) \
                        values(:1, :2, :3, :4, :5, :6, :7, \
                        TO_DATE(:8,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:9,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:10,'YYYY-MM-DD HH24:MI:SS'), :11, :12)", rows)
        connection.commit()
    except:
        pass
    page += 1
 
        

