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
    url = baseURL+"devices"#?filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from Devices API to Devices
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Devices:
    in_use : str
    code : str
    device_id : str
    name : str
    reference : str
    type : str
    latitude : str
    longitude : str
    model : str
    build : str
    app_version : str
    system_version : str
    is_online_receiver : str
    is_blocked : str
    last_sync_at : datetime
    last_seen_at  : datetime
    last_order_at  : datetime
    created_at  : datetime
    updated_at  : datetime
    deleted_at  : datetime
    first_activation_at : datetime

#cursor.execute("truncate table Devices")
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
            print(1)
            Devices.in_use = item["in_use"]
            Devices.code  = item["code"]
            Devices.device_id  = item["id"]
            Devices.name  = item["name"]
            Devices.reference  = item["reference"]
            Devices.type  = item["type"]
            Devices.latitude  = item["latitude"]
            Devices.longitude  = item["longitude"]
            Devices.model  = item["model"]
            Devices.build  = item["build"]
            Devices.app_version  = item["app_version"]
            Devices.system_version  = item["system_version"]
            Devices.is_online_receiver  = item["is_online_receiver"]
            Devices.is_blocked  = item["is_blocked"]
            Devices.last_sync_at = item["last_sync_at"]
            Devices.last_seen_at  = item["last_seen_at"]
            Devices.last_order_at  = item["last_order_at"]
            Devices.created_at  = item["created_at"]
            Devices.updated_at  = item["updated_at"]
            Devices.deleted_at  = item["deleted_at"]
            Devices.first_activation_at  = item["first_activation_at"]
            print(2)

            tuple_data_details = ( 
                                    Devices.in_use
                                    ,Devices.code
                                    ,Devices.device_id
                                    ,Devices.name
                                    ,Devices.reference
                                    ,Devices.type
                                    ,Devices.latitude
                                    ,Devices.longitude
                                    ,Devices.model
                                    ,Devices.build
                                    ,Devices.app_version
                                    ,Devices.system_version
                                    ,Devices.is_online_receiver
                                    ,Devices.is_blocked
                                    ,Devices.last_sync_at
                                    ,Devices.last_seen_at 
                                    ,Devices.last_order_at 
                                    ,Devices.created_at 
                                    ,Devices.updated_at 
                                    ,Devices.deleted_at 
                                    ,Devices.first_activation_at
                                )

            rows.append(tuple_data_details)
    except:
        pass
    
    print(rows)
    try:
        cursor.executemany("insert into Devices ( \
                                    Devices.in_use\
                                    ,Devices.code\
                                    ,Devices.device_id\
                                    ,Devices.name\
                                    ,Devices.reference\
                                    ,Devices.type\
                                    ,Devices.latitude\
                                    ,Devices.longitude\
                                    ,Devices.model\
                                    ,Devices.build\
                                    ,Devices.app_version\
                                    ,Devices.system_version\
                                    ,Devices.is_online_receiver\
                                    ,Devices.is_blocked\
                                    ,Devices.last_sync_at\
                                    ,Devices.last_seen_at \
                                    ,Devices.last_order_at \
                                    ,Devices.created_at \
                                    ,Devices.updated_at \
                                    ,Devices.deleted_at \
                                    ,Devices.first_activation_at) \
                        values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, \
                        TO_DATE(:15,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:16,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:17,'YYYY-MM-DD HH24:MI:SS'), \
                        TO_DATE(:18,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:19,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:20,'YYYY-MM-DD HH24:MI:SS'),\
                        TO_DATE(:21,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    page += 1
 
        

