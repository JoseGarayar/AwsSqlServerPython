#!/usr/bin/env python

import pyodbc   # connection to sql server
from Adafruit_BME280 import * 
import time
import random #Pruebas
from CredentialsAws import Credentials

# data to access to data base
# Add your own data here
server = Credentials.server
database = Credentials.database
username = Credentials.username
password = Credentials.password
port=Credentials
TDS_Version='7.3'
driver = 'FreeTDS'
tablename = Credentials.tablename

date = time.strftime("%b %d %Y %H:%M%p") #Formato SQL server

con_string='UID=%s;PWD=%s;DATABASE=%s;PORT=%s;TDS=%s;SERVER=%s;driver=%s' %(username,password,database,port,TDS_Version,server,driver)

cnxn=pyodbc.connect(con_string)
cursor=cnxn.cursor()
cmd = "insert into %s (Temp, Hum, Presion, Fechahora) values(?,?,?,?)" %tablename

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()
cursor.execute(cmd, (degrees, humidity, hectopascals, date))

#x1 = random.uniform(20,25)
#x2 = random.uniform(65,75)
#x3 = random.uniform(995,1005)
#cursor.execute(cmd, (x1, x2, x3, date))

cursor.close()
cnxn.commit()
