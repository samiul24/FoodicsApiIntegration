import os
import oracledb
from dotenv import load_dotenv
from pathlib import Path

env_path = os.path.dirname(__file__)
env_path = os.path.join(os.path.dirname(env_path), "Conn",".env").replace('\\','/')
load_dotenv(dotenv_path=Path(env_path))

user = os.environ.get("user")
password = os.environ.get("password")
dsn = os.environ.get("dsn")

def connect_to_oracle():
    try:
        connection = oracledb.connect(user=user,password=password,dsn=dsn)
        return connection
    except:
        return "Connection error!"