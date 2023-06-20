print('check.py-execute')
#firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Raspbeery
import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


try:
    app = firebase_admin.get_app()
except:
    cred = credentials.Certificate("smartfarmbase-firebase-adminsdk-8vmv8-5f0892865a.json")
    firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://smartfarmbase-default-rtdb.firebaseio.com/smartfarm'
    })

check_ref = db.reference('Check')

while True:
    try:
        check = check_ref.get()
        if check == 1:
            GPIO.output(18, True)
            break;
    except: 
        GPIO.output(18, False)


def thread_run():
    GPIO.output(18, False)
    threading.Timer(10, thread_run).start()

thread_run()

while True:
    try:
        check = check_ref.get()
    except:
        pass
    if check == 1:
        GPIO.output(18, True)

