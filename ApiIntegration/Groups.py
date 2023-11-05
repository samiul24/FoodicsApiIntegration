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
    url = baseURL+"groups?include=products"#&filter[created_on]="+previous_date
    #print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from Groups API to Groups
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Groups:
    group_id: str
    name: str
    name_localized: str
    items_index: str
    product_id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

#cursor.execute("truncate table Groups")
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
            else:
                time.sleep(60)
                current_attempt_m +=1

        except:
            time.sleep(60)
            current_attempt_m +=1

    objects = responseData["data"]
    if len(objects)==0:
        exit()
        
    rows = []
    try:
        for item in responseData["data"]:
            Groups.group_id = item["id"]
            Groups.name = item["name"]
            Groups.name_localized = item["name_localized"]
            Groups.items_index = str(item["items_index"])
            Groups.created_at = item["created_at"]
            Groups.updated_at= item["updated_at"]
            Groups.deleted_at= item["deleted_at"]

            if item["products"]!=None and len(item["products"])>0:
                for product in item["products"]:
                    Groups.product_id = product["id"]
                    tuple_data_details = ( 
                                Groups.group_id,
                                Groups.name,
                                Groups.name_localized,
                                Groups.items_index,
                                Groups.product_id,
                                Groups.created_at,
                                Groups.updated_at,
                                Groups.deleted_at
                                )

                    rows.append(tuple_data_details)
            else:
                Groups.product_id = ''
                tuple_data_details = ( 
                                    Groups.group_id,
                                    Groups.name,
                                    Groups.name_localized,
                                    Groups.items_index,
                                    Groups.product_id,
                                    Groups.created_at,
                                    Groups.updated_at,
                                    Groups.deleted_at
                                    )

                rows.append(tuple_data_details)
    except:
        pass
    
    #print(rows)
    cursor.executemany("insert into Groups ( \
                                                Groups.group_id,\
                                                Groups.name,\
                                                Groups.name_localized,\
                                                Groups.items_index,\
                                                Groups.product_id,\
                                                Groups.created_at,\
                                                Groups.updated_at,\
                                                Groups.deleted_at\
                                               ) \
                        values(:1, :2, :3, :4, :5, \
                        TO_DATE(:6,'YYYY-MM-DD HH24:MI:SS'), \
                        TO_DATE(:7,'YYYY-MM-DD HH24:MI:SS'),\
                        TO_DATE(:8,'YYYY-MM-DD HH24:MI:SS'))", rows)
    connection.commit()
   
    page += 1
 
        

