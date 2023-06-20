print('OutTempHum.py-execute')
#firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Raspbeery
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep

#Python
import threading

try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("smartfarmbase-firebase-adminsdk-8vmv8-5f0892865a.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://smartfarmbase-default-rtdb.firebaseio.com/smartfarm'
        })
    
Hum_ref = db.reference()
Temp_ref = db.reference()

sensor = Adafruit_DHT.DHT11
    
GPIO.setwarnings(False)

while True:
    hum, temp = Adafruit_DHT.read_retry(sensor, 4)
    if hum is not None and temp is not None:
        if((int(hum) >= 0 and int(hum) <= 100) and (int(temp) >= 0 and int(temp) <= 100)):
            try:
                Hum_ref.update({'OutHum':int(hum)})
                Temp_ref.update({'OutTemp':int(temp)})
            except:
                print('error')
    else:
        print('fail')
    sleep(1)
    

