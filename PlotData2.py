#!/usr/bin/env python
# -*- coding: cp1252 

# libraries
# import smbus    # permite la comunicacion I2C entre el raspberry y el MPU
import math     
import time     # library for time tools
import pyodbc   # connection to sql server
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.dates import DayLocator, MinuteLocator,HourLocator,DateFormatter
from numpy import arange
from CredentialsAws import Credentials


def plotData(fig,ax,Data=[],yMin=0,yMax=0,title='',ylabel=''):
    ax.plot_date(Date1, Data, '-b')
    ax.set_ylim(yMin,yMax)

    ax.set_title(title)
    ax.set_xlabel('Fecha y hora')
    ax.set_ylabel(ylabel)

    #ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_minor_locator(HourLocator(arange(0 , 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d \n %H:%M'))
    ax.grid(True)


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
    for row in rows:
        Temp1.append(row.Temp)
        Hum1.append(row.Hum)
        Presion1.append(row.Presion)
        Date1.append(row.Fechahora)

else:
    print "NO DATA."

cursor.close()
cnxn.commit()

fig1, ax1 = plt.subplots()
plotData(fig1,ax1,Temp1,yMin=0,yMax=50,title='BME280 - Temperatura',ylabel='Temperatura ($^\circ$C)')

fig2, ax2 = plt.subplots()
plotData(fig2,ax2,Hum1,yMin=0,yMax=100,title='BME280 - Humedad',ylabel='Humedad (%)')

fig3, ax3 = plt.subplots()
plotData(fig3,ax3,Presion1,yMin=900,yMax=1100,title='BME280 - Presion',ylabel='Presion (HPa)')

plt.show()
