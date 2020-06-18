
#!/usr/bin/env python
# -*- coding: cp1252 
'''Executable on Windows'''
# libraries
# import smbus    # permite la comunicacion I2C entre el raspberry y el MPU
import math     
import time     # library for time tools
import pyodbc   # connection to sql server
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.dates import DayLocator, HourLocator,DateFormatter,MinuteLocator
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

con_string='UID=%s;PWD=%s;DATABASE=%s;PORT=%s;TDS=%s;SERVER=%s;driver=%s' %(username,password,database,port,TDS_Version,server,driver)
cnxn=pyodbc.connect(con_string)
cursor=cnxn.cursor()

''' type the table name here '''
tablename = 'Sensores1'
cmd ="select * from %s" %tablename

tb = cursor.execute(cmd)
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
        Date1.append(row.FechaHora)

else:
    print "NO DATA."

while True:
    dato = int(raw_input('Seleccione el tipo de dato:\n 1.Temperatura\n 2.Humedad\n 3.Presion\n'))
    if dato == 1:
        text = Temp1
        text2 = 'Temp'
        break
    elif dato == 2:
        text = Hum1
        text2 = 'Hum'
        break
    elif dato == 3:
        text = Pres1
        text2 = 'Pres'
        break
    else:
        print "No ingreso un dato valido\n"


print "plotting..."

#style.use('fivethirtyeight')
style.use('ggplot')

fig, ax = plt.subplots()
ax.set_title('Pruebas')
plt.xlabel('Fecha y hora')
plt.ylabel(text2)
ax.set_ylim(0,100)
ax.xaxis.set_major_locator(HourLocator(arange(0,24,1)))
ax.xaxis.set_minor_locator(MinuteLocator(arange(0,60,5)))
ax.xaxis.set_major_formatter(DateFormatter("\n%Y-%m-%d"))
ax.xaxis.set_minor_formatter(DateFormatter('%H:%M'))
'''ax.set_title('Tanque de Prueba en lancha: Maca')
ax.plot_date(date, level, '-bs', markersize = 3)
ax.set_xlabel('Fecha y hora')
ax.set_ylabel('Nivel de combustible [cm]')
ax.set_ylim(0,60)
ax.xaxis.set_major_locator(DayLocator())
ax.xaxis.set_minor_locator(HourLocator(arange(0,25,6)))
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d ___'))
ax.xaxis.set_minor_formatter(DateFormatter('%H:%M'))'''

def animate(i):
            
        com = "Select * from %s where Id = (select max(Id) from %s)" %(tablename,tablename)
        nw = cursor.execute(com) 
        nw = nw.fetchone()
        current_date = str(nw.FechaHora)
        current_date = current_date.split(' ')
        [h,m,s] = current_date[1].split(':')
        
        if time.strftime("%H")==h and time.strftime("%M") == m:
            Date1.append(nw.FechaHora)
            if dato == 1:
                text.append(nw.Temp)
            if dato == 2:
                text.append(nw.Hum)
            if dato == 3:
                text.append(nw.Pres)
        ax.plot_date(Date1, text, 'b-', markersize = 1)
ani = animation.FuncAnimation(fig, animate, interval=1000)

ax.grid(True)
plt.show()
cursor.close()
cnxn.commit()
print "...\n****closing program****"




