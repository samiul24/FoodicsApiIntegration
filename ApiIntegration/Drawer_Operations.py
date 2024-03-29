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
    url = baseURL+"drawer_operations?filter[created_on]="+previous_date
    print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from drawer_operations API to drawer_operations
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class drawer_operations:
    drawer_operation_id: str
    type: float
    amount: float
    notes: str
    recorded_at: datetime
    created_at: datetime
    updated_at: datetime

#cursor.execute("truncate table drawer_operations")
cursor.execute("insert into Run_Log(API_Name) values('Drawer_Operations')")
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
            else:
                time.sleep(60)
                current_attempt_m +=1

        except:
            time.sleep(60)
            current_attempt_m +=1

    try:
        objects = responseData["data"]
    except:
        exit()

    if len(objects)==0:
        exit()
        
    rows = []
    try:
        for item in responseData["data"]:
            drawer_operations.drawer_operation_id = item["id"]
            drawer_operations.type = item["type"]         
            drawer_operations.amount = item["amount"]                  
            drawer_operations.notes = item["notes"]
            drawer_operations.created_at = item["created_at"]
            drawer_operations.updated_at = item["updated_at"]

            tuple_data_details = ( 
                                    drawer_operations.drawer_operation_id,
                                    drawer_operations.type,
                                    drawer_operations.amount,
                                    drawer_operations.notes,                
                                    drawer_operations.created_at,
                                    drawer_operations.updated_at

                                )

            rows.append(tuple_data_details)
    except:
        pass

    try:
        cursor.executemany("insert into drawer_operations ( drawer_operations.drawer_operation_id,\
                                                            drawer_operations.type, \
                                                            drawer_operations.amount, \
                                                            drawer_operations.notes, \
                                                            drawer_operations.created_at, \
                                                            drawer_operations.updated_at) \
                        values(:1, :2, :3, :4, \
                        TO_DATE(:5,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:6,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    page += 1
 
        

