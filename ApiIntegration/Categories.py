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
    url = baseURL+"categories?filter[created_on]="+previous_date
    print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Purchase Order API to Categories
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Categories:
    category_id: str
    name: str
    name_localized: str
    reference: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

#cursor.execute("truncate table Categories")
cursor.execute("insert into Run_Log(API_Name) values('Categories')")
page = 1
while True:
    params = {'page': page, 'per_page': 50}
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
            Categories.category_id = item["id"]
            Categories.name = item["name"]
            Categories.name_localized = item["name_localized"]
            Categories.reference = item["reference"]
            Categories.created_at = item["created_at"]
            Categories.updated_at = item["updated_at"]
            Categories.deleted_at = item["deleted_at"]

            tuple_data_details = (Categories.category_id, Categories.name, Categories.name_localized, 
                                Categories.reference, Categories.created_at, Categories.updated_at, 
                                Categories.deleted_at
                                )
            rows.append(tuple_data_details)
    except:
        pass
    
    print(rows)
    try:
        cursor.executemany("insert into Categories (category_id, name, name_localized, reference, \
                                                          created_at, updated_at, deleted_at) \
                        values(:1, :2, :3, :4, \
                        TO_DATE(:5,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:6,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:7,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    
    page +=1
 
        

