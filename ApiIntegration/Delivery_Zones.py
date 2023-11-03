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
    url = baseURL+"delivery_zones?filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from delivery_zones API to delivery_zones
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class delivery_zones:
    delivery_zone_id: str
    name: str
    name_localized: str
    reference: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    branch_id: str

#cursor.execute("truncate table delivery_zones")
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
    try:
        for item in responseData["data"]:
            delivery_zones.delivery_zone_id = item["id"]     
            delivery_zones.name = item["name"]         
            delivery_zones.name_localized = item["details"]            
            delivery_zones.reference = item["description"]    
            delivery_zones.created_at = item["created_at"]
            delivery_zones.updated_at = item["updated_at"]
            delivery_zones.deleted_at = item["deleted_at"]
            

            if item["branches"]!=None and len(item["branches"])>0:
                delivery_zones.branch_id = item["branches"][0]["id"]
            else:
                delivery_zones.branch_id = ''

            tuple_data_details = ( 
                                    delivery_zones.delivery_zone_id,
                                    delivery_zones.name,
                                    delivery_zones.name_localized,        
                                    delivery_zones.reference,     
                                    delivery_zones.branch_id,  
                                    delivery_zones.created_at,
                                    delivery_zones.updated_at,
                                    delivery_zones.deleted_at
                                    
                                )

            rows.append(tuple_data_details)
    except:
        pass

    try:
        cursor.executemany("insert into delivery_zones (delivery_zones.delivery_zone_id,\
                                                        delivery_zones.name, \
                                                        delivery_zones.name_localized, \
                                                        delivery_zones.reference, \
                                                        delivery_zones.branch_id,  \
                                                        delivery_zones.created_at, \
                                                        delivery_zones.updated_at, \
                                                        delivery_zones.deleted_at) \
                        values(:1, :2, :3, :4, :5, \
                        TO_DATE(:6,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:7,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:7,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    page += 1
 
        

