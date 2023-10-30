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
    url = baseURL+"addresses?include=customer,delivery_zone&filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from Addresses API to Addresses
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Addresses:
    addresses_id: str
    city_id: str
    name: str
    details: str
    description: str
    latitude: str
    longitude: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    customer_id: str
    delivery_zone_id: str

#cursor.execute("truncate table Addresses")
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
            Addresses.addresses_id = item["id"]
            Addresses.city_id = item["city_id"]         
            Addresses.name = item["name"]         
            Addresses.details = item["details"]            
            Addresses.description = item["description"]
            Addresses.latitude = item["latitude"]            
            Addresses.longitude = item["longitude"]            
            Addresses.created_at = item["created_at"]
            Addresses.updated_at = item["updated_at"]
            Addresses.deleted_at = item["deleted_at"]
            

            if item["customer"]!=None and len(item["customer"])>0:
                Addresses.customer_id = item["customer"]["id"]
            else:
                Addresses.customer_id = ''

            if item["delivery_zone"]!=None and len(item["delivery_zone"])>0:
                Addresses.delivery_zone_id = item["delivery_zone"]["id"]
            else:
                Addresses.delivery_zone_id = ''

            tuple_data_details = ( 
                                    Addresses.addresses_id,
                                    Addresses.city_id,
                                    Addresses.name,
                                    Addresses.details,        
                                    Addresses.description,
                                    Addresses.latitude,   
                                    Addresses.longitude,         
                                    Addresses.created_at,
                                    Addresses.updated_at,
                                    Addresses.deleted_at,
                                    Addresses.customer_id,
                                    Addresses.delivery_zone_id
                                )

            rows.append(tuple_data_details)
    except:
        pass

    try:
        cursor.executemany("insert into Addresses (Addresses.addresses_id, Addresses.city_id, Addresses.name, \
                                                   Addresses.details, Addresses.description, Addresses.latitude, \
                                                   Addresses.longitude, Addresses.created_at, Addresses.updated_at, Addresses.deleted_at,\
                                                   Addresses.customer_id, Addresses.delivery_zone_id) \
                        values(:1, :2, :3, :4, :5, :6, :7, \
                        TO_DATE(:8,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:9,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:10,'YYYY-MM-DD HH24:MI:SS'), :11, :12)", rows)
        connection.commit()
    except:
        pass
    page += 1
 
        

