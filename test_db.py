import os
from sqlalchemy import create_engine

user = os.environ['DB_USER']
password = os.environ['DB_PASS']
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']
db = os.environ['DB_NAME']

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT NOW()")
        print("Conexión exitosa:", list(result))
except Exception as e:
    print("Error de conexión:", e)

