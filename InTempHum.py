print('InHumTemp.py-execute')
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
    

    
FB_ref = db.reference()

mode_ref = db.reference('Mode')
Fan_read = db.reference('Fan')
Light_read = db.reference('Light')

FB_Change = db.reference('Change')
Change = 0

FB_HighTemp = db.reference('HighTemp')
FB_LowTemp = db.reference('LowTemp')
FB_HighHum = db.reference('HighHum')
HT = 0
LT = 0
HH = 0

sensor = Adafruit_DHT.DHT22
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

mode = 0

GPIO.output(5, True)
GPIO.output(6, True)

def connectFB(): #connect internet
    while True:
        hum, temp = Adafruit_DHT.read_retry(sensor, 2)
        try:
            global Change
            global mode
            Change = FB_Change.get()
            if(Change == 1):
                HT_write = open('HighTemp.txt','w')
                HT_write.write(str(FB_HighTemp.get()))
                HT_write.close()
                
                LT_write = open('LowTemp.txt','w')
                LT_write.write(str(FB_LowTemp.get()))
                LT_write.close()
                
                HH_write = open('HighHum.txt','w')
                HH_write.write(str(FB_HighHum.get()))
                HH_write.close()
                
                Change = 0
                FB_ref.update({'Change': 0})
            
                
            mode = mode_ref.get()
            if mode == 1:
                FAN = Fan_read.get()
                LED = Light_read.get()
                if(FAN == 1):
                    GPIO.output(6, True)
                if(FAN == 0):
                    GPIO.output(6, False)
                    
                if(LED == 1):
                    GPIO.output(5, True)
                    
                if(LED == 0):
                    GPIO.output(5, False)
        except:
            print('error1')
            
            
        if hum is not None and temp is not None:
            if((int(hum) >= 0 and int(hum) <= 100) and (int(temp) >= 0 and int(temp) <= 100)):
                try:
                    FB_ref.update({'InHum':int(hum)})
                    FB_ref.update({'InTemp':int(temp)})
                except:
                    print('error2')
        sleep(1)

def thread_run():
    global mode
    mode = 0
    try:
        FB_ref.update({'Mode':0})
    except:
        print('error3')
    threading.Timer(40, thread_run).start()

t_work = threading.Thread(target=connectFB)
t_work.start()
thread_run()

while True:
    hum, temp = Adafruit_DHT.read_retry(sensor, 2)
    if hum is not None and temp is not None:
        hum = int(hum)
        temp = int(temp)
    else:
        print('fail')
        
    if(Change == 0):
        HT_read = open('HighTemp.txt', 'r')
        HT = HT_read.readline()
        HT_read.close()
            
        LT_read = open('LowTemp.txt', 'r')
        LT = LT_read.readline()
        LT_read.close()
            
        HH_read = open('HighHum.txt', 'r')
        HH = HH_read.readline()
        HH_read.close()
            
    if(mode == 0):
        if((hum >= 0 and hum <= 100) and (temp >= 0 and temp <= 100)):
            if(temp > int(HT) or hum > int(HH)):
                GPIO.output(6, True)
            if(temp <= int(HT)-2 and hum <= int(HH)-10):
                GPIO.output(6, False)
            if(temp <= int(HT)):
                GPIO.output(5, True)
            if(temp > int(HT) + 1):
                GPIO.output(5, False)
    sleep(1)
