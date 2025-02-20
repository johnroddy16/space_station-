#!/usr/bin/env python3 

import requests
from datetime import datetime as dt 
import smtplib 
from time import sleep 

MY_LAT = 47.606209 # seattle latitude
MY_LONG = -122.332069 # seattle longitude   

response = requests.get(url='http://api.open-notify.org/iss-now.json')
response.raise_for_status()
data = response.json()

iss_latitude = float(data['iss_position']['latitude'])
iss_longitude = float(data['iss_position']['longitude']) 

parameters = {
    'lat': MY_LAT,
    'lng': MY_LONG,
    'formatted': 0,
}

response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
print(sunrise, sunset)

time_now = dt.now().hour  

# dark: 
def dark(cur_time, sett, rise):
    if cur_time >= sett or cur_time <= rise:
        return True 
    return False 

# close:
def close(lat, lng, iss_lat, iss_lng):
    if lat - 5 <= iss_lat <= lat + 5 and lng - 5 <= iss_lng <= lng + 5:
        return True 
    return False 

dark = dark(time_now, sunset, sunrise)
close = close(MY_LAT, MY_LONG, iss_latitude, iss_longitude)

# make the program run every 60 seconds:
while True:
    sleep(60)
    if dark and close:
        email = 'nohtyp742@gmail.com'
        password = 'not a real password'
        
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            # make the connection secure:
            connection.starttls()  
            # login to email:
            connection.login(user=email, password=password)
            # send the email: 
            connection.sendmail(from_addr=email, to_addrs='johnroddy.16@gmail.com', msg=f'subject:ISS!!!!\n\nLook Up!!!!')
