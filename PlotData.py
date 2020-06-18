#!/usr/bin/env python
# -*- coding: cp1252 

# libraries
# import smbus    # permite la comunicacion I2C entre el raspberry y el MPU
import math     
import time     # library for time tools
import pyodbc   # connection to sql server
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.dates import DayLocator, HourLocator,DateFormatter
from numpy import arange
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

con_string='UID=%s;PWD=%s;DATABASE=%s;PORT=%s;TDS=%s;SERVER=%s;driver=%s' % (username,password,database,port,TDS_Version,server,driver)
cnxn=pyodbc.connect(con_string)
cursor=cnxn.cursor()
tb = cursor.execute("select Temp, Hum, Presion, Fechahora from Sensores1")

rows = tb.fetchall()

Temp1 = []
Hum1 = []
Presion1 = []
Date1 = []

if rows is not None:
    i = 0
    id_date = 0
    for row in rows:
        Temp1.append(row.Temp)
        Hum1.append(row.Hum)
        Presion1.append(row.Presion)
        Date1.append(row.Fechahora)

else:
    print "NO DATA."

#t = range(len(data_vibration)) 
cursor.close()

fig, ax = plt.subplots()
#ax.plot_date(Date1, Temp1, '-b')
ax.plot_date(Date1, Hum1, '-b')
#ax.plot_date(Date1, Presion1, '-b')
ax.set_ylim(0,80)

ax.set_title('Temperatura')
ax.set_xlabel('Fecha y hora')
ax.set_ylabel('Temp')

ax.xaxis.set_major_locator(DayLocator())
ax.xaxis.set_minor_locator(HourLocator(arange(0 , 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d ___'))
ax.xaxis.set_minor_formatter(DateFormatter('%H:%M'))
ax.grid(True)
ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
fig.autofmt_xdate()

'''
#fig1, ax = plt.subplots()
#ax.plot_date(t[1466:len(t) + 1], data_vibration[1466:len(data_vibration) + 1], '-b')
#ax.plot_date(t, data_vibration, '-b')

#ax.set_xlim(t[0], t[-1])
ax.set_title('Niveles de vibracion')
ax.set_xlabel('Fecha y hora')
ax.set_ylabel('Nivel de vibracion')

ax.xaxis.set_major_locator(DayLocator())
ax.xaxis.set_minor_locator(HourLocator(arange(0 , 25, 3)))
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d ___'))
ax.xaxis.set_minor_formatter(DateFormatter('%H:%M'))
ax.grid(True)
ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
fig1.autofmt_xdate()
'''
plt.show()
