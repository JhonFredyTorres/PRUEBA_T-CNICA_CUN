# Proyecto ETL - COVID CUN 

Este proyecto realiza una carga automática de archivos CSV con información de casos COVID hacia una base de datos MySQL en la nube (AWS RDS), desde una instancia EC2.

---
# Configuración de Acceso AWS

## Credenciales de Acceso

**Nota importante:** Estas credenciales son confidenciales. No las comparta ni las incluya en repositorios públicos.

- **Consola AWS:** https://594239945667.signin.aws.amazon.com/console
- **Usuario:** etl_user
- **Contraseña:** Test2025*!

## Requisitos de Configuración de Red

Para acceder a los recursos del proyecto, es necesario configurar correctamente los permisos de red:

### 1. Configuración de EC2

Antes de conectarse, es necesario agregar la dirección IP de su equipo a los grupos de seguridad correspondientes:

1. Inicie sesión en la consola AWS
2. Navegue a EC2 → Grupos de seguridad → `Servidor_sh`
3. Seleccione la pestaña "Reglas de entrada"
4. Haga clic en "Editar reglas de entrada"
5. Añada una nueva regla con:
   - Tipo: SSH (puerto 22)
   - Origen: Su dirección IP pública
   - Descripción: Su nombre (ej. "Juan Perez")

### 2. Configuración de RDS MySQL

Para conectarse a la base de datos MySQL:

1. Navegue a RDS → Grupos de seguridad → `bdMYSQL`
2. Seleccione la pestaña "Reglas de entrada"
3. Haga clic en "Editar reglas de entrada"
4. Añada una nueva regla con:
   - Tipo: MySQL/Aurora (puerto 3306)
   - Origen: Su dirección IP pública
   - Descripción: Su nombre  (ej. "Juan Perez")

## Proceso de Conexión

1. Una vez añadida su IP a los grupos de seguridad, podrá:
   - Conectarse al servidor EC2 mediante SSH o herramientas como PuTTY
   - Conectarse a la base de datos MySQL usando clientes como MySQL Workbench, DBeaver o Tableau



##  Acceso al servidor EC2

1. Descargar el archivo `.pem` de acceso:
   - Asegúrate de tener el archivo `Test.pem` en tu máquina local.

2. Conéctate al servidor EC2:

```bash
ssh -i ~/Downloads/Test.pem ec2-user@54.70.168.147


3. Cambia al usuario biops:
sudo su biops
cd

##Estructura del proyecto:###

/home/biops/
├── .lib/               ← Variables sensibles (vm.sh con claves)
│   └── vm.sh
├── data/               ← Archivos CSV de entrada
├── etl/                ← Script de carga y entorno virtual
│   └── carga_datos.py
├── logs/               ← Logs de ejecución del ETL


###Requisitos del entorno###

Python 3.9

Entorno virtual (/home/biops/etl/env/)

####Paquetes:###

mysql-connector-python

python-dotenv

###Crontab:####  
6 * * * * /home/biops/etl/env/bin/python /home/biops/etl/carga_datos.py >> /home/biops/logs/carga_datos.py.log 2>&1

####Ejecutar el ETL manualmente:#####

cd /home/biops/etl
source env/bin/activate
python carga_datos.py

Automaticamente: 

Elimina datos existentes.

Inserta nuevos desde /home/biops/data/*.csv.

Guarda logs en /home/biops/logs/carga_datos.log.

###Visualización en Tableau: #####

https://public.tableau.com/views/Covid_cun/COVID?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

###Conexión a la base de datos:####

Host: covid-db.c30geciwy8u3.us-west-2.rds.amazonaws.com

Base de datos: covid_db

Usuario: tableau_user

Contraseña: Jh0n15$&

Permisos: Solo lectura (SELECT)

## S3

url: https://us-west-2.console.aws.amazon.com/s3/home?region=us-west-2  mismas credenciales de aws para poder ingresar al BUCKET.

###Autor:#####

Jhon Fredy Torres Peña
jhonfredytorresp@gmail.com

