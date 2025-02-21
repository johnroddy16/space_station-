#!/usr/bin/env python3 

import requests
from datetime import datetime as dt 
import smtplib 
from time import sleep 

MY_LAT = 47.606209 # seattle latitude
MY_LONG = -122.332069 # seattle longitude  

email = 'nohtyp742@gmail.com'
password = 'xddewbafczduzurt'    

# dark: 
def dark():
    parameters = {
    'lat': MY_LAT,
    'lng': MY_LONG,
    'formatted': 0,
    }
    
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0]) - 8 # time comes back in UTC
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0]) + 16
    
    time_now = dt.now().hour
    
    if time_now >= sunset or time_now  <= sunrise:
        return True  

# close:
def close():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])
    
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True  

# make the program run every 60 seconds:
while True:
    sleep(60) 
    
    darkk = dark()
    closee = close()
    
    if darkk and closee:
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            # make the connection secure:
            connection.starttls()  
            # login to email:
            connection.login(user=email, password=password)
            # send the email: 
            connection.sendmail(from_addr=email, to_addrs='johnroddy.16@gmail.com', msg=f'subject:ISS!!!!\n\nLook Up!!!!')
    