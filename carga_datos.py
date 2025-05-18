import os
import csv
from datetime import datetime
import mysql.connector
import boto3
from dotenv import load_dotenv

# variables de entorno
load_dotenv('/home/biops/.lib/vm.sh')

# BD
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

#  S3
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_REGION = os.getenv("S3_REGION")

# Fecha actual
today = datetime.now()
year = today.strftime('%Y')
month = today.strftime('%m')
day = today.strftime('%d')

# Nombres de archivos
filename_metricas = f"metricas_covid-{day}.csv"
filename_edades = f"edades_covid-{day}.csv"
local_path_metricas = f"/home/biops/data/{filename_metricas}"
local_path_edades = f"/home/biops/data/{filename_edades}"

s3_key_metricas = f"{year}/{month}/{filename_metricas}"
s3_key_edades = f"{year}/{month}/{filename_edades}"

# Conexión MySQL
conn = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)
cursor = conn.cursor()

# Creación de archivos de  métricas 
with open(local_path_metricas, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "total"])

    cursor.execute("SELECT 'Contagios', COUNT(*) FROM cases")
    writer.writerow(cursor.fetchone())

    cursor.execute("""
        SELECT 'Recuperado', COUNT(*)
        FROM cases c JOIN status s ON c.id_status = s.id_status
        WHERE s.name = 'Recuperado'
    """)
    writer.writerow(cursor.fetchone())

    cursor.execute("""
        SELECT 'Fallecido', COUNT(*)
        FROM cases c JOIN status s ON c.id_status = s.id_status
        WHERE s.name = 'Fallecido'
    """)
    writer.writerow(cursor.fetchone())

    cursor.execute("""
        SELECT 'promedio_dias_recuperacion', ROUND(AVG(DATEDIFF(date_recovery, date_symptom)), 2)
        FROM cases
        WHERE date_symptom IS NOT NULL AND date_recovery IS NOT NULL
    """)
    writer.writerow(cursor.fetchone())

# Crear archivo edades
with open(local_path_edades, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Edad", "Porcentaje Fallecidos"])
    cursor.execute("""
        SELECT 
            CONCAT(FLOOR(age / 10) * 10, 's'),
            CONCAT(ROUND(SUM(CASE WHEN date_death IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2), '%')
        FROM cases
        WHERE age IS NOT NULL
        GROUP BY FLOOR(age / 10)
        ORDER BY FLOOR(age / 10)
    """)
    for row in cursor.fetchall():
        writer.writerow(row)

# Subir a S3
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION
)

try:
    s3.upload_file(local_path_metricas, S3_BUCKET, s3_key_metricas)
    s3.upload_file(local_path_edades, S3_BUCKET, s3_key_edades)
    print(f"✅ Archivos subidos correctamente a S3:\n - {s3_key_metricas}\n - {s3_key_edades}")
except Exception as e:
    print(f"❌ Error al subir archivos a S3: {e}")

cursor.close()
conn.close()

