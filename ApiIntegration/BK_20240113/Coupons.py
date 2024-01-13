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
    url = baseURL+"coupons?include=discount"#&filter[created_on]="+previous_date
    print(url)
    Authorization = os.environ.get("Authorization")
except:
    pass

#data load from List Coupons API to Coupons
payload = {}
headers = {
  'Authorization': Authorization,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

@dataclass
class Coupons:
    coupon_id: str
    name: str
    code: str
    maximum_uses: str
    is_active: str
    is_sat: str
    is_sun: str
    is_mon: str
    is_tue: str
    is_wed: str
    is_thu: str
    is_fri: str
    discount_id: str
    from_date: datetime
    to_date: datetime
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

cursor.execute("truncate table Coupons")
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
            Coupons.coupon_id = item["id"]
            Coupons.name = item["name"]
            Coupons.code = item["code"]
            Coupons.maximum_uses = item["maximum_uses"]
            Coupons.is_active = item["is_active"]
            Coupons.is_sat = item["is_sat"]
            Coupons.is_sun = item["is_sun"]
            Coupons.is_mon = item["is_mon"]
            Coupons.is_tue = item["is_tue"]
            Coupons.is_wed = item["is_wed"]
            Coupons.is_thu = item["is_thu"]
            Coupons.is_fri = item["is_fri"]
            Coupons.discount_id = item["discount"]["id"]
            Coupons.from_date = item["from_date"]
            Coupons.to_date = item["to_date"]
            Coupons.created_at = item["created_at"]
            Coupons.updated_at = item["updated_at"]
            Coupons.deleted_at = item["deleted_at"]

            tuple_data_details = (
                                    Coupons.coupon_id 
                                    ,Coupons.name 
                                    ,Coupons.code 
                                    ,Coupons.maximum_uses 
                                    ,Coupons.is_active 
                                    ,Coupons.is_sat 
                                    ,Coupons.is_sun 
                                    ,Coupons.is_mon 
                                    ,Coupons.is_tue 
                                    ,Coupons.is_wed 
                                    ,Coupons.is_thu 
                                    ,Coupons.is_fri 
                                    ,Coupons.discount_id 
                                    ,Coupons.from_date 
                                    ,Coupons.to_date 
                                    ,Coupons.created_at
                                    ,Coupons.updated_at
                                    ,Coupons.deleted_at 
                                                        )
            rows.append(tuple_data_details)
    except:
        pass
    
    print(rows)
    try:
        cursor.executemany("insert into Coupons ( \
                                                Coupons.coupon_id      \
                                                ,Coupons.name           \
                                                ,Coupons.code           \
                                                ,Coupons.maximum_uses   \
                                                ,Coupons.is_active      \
                                                ,Coupons.is_sat         \
                                                ,Coupons.is_sun         \
                                                ,Coupons.is_mon         \
                                                ,Coupons.is_tue         \
                                                ,Coupons.is_wed         \
                                                ,Coupons.is_thu         \
                                                ,Coupons.is_fri         \
                                                ,Coupons.discount_id    \
                                                ,Coupons.from_date      \
                                                ,Coupons.to_date        \
                                                ,Coupons.created_at     \
                                                ,Coupons.updated_at     \
                                                ,Coupons.deleted_at )   \
                        values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, \
                        TO_DATE(:14,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:15,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:16,'YYYY-MM-DD HH24:MI:SS'),\
                        TO_DATE(:17,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:18,'YYYY-MM-DD HH24:MI:SS'))", rows)
        connection.commit()
    except:
        pass
    
    page +=1
 
        

