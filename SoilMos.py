print('SoilMos.py-execute')

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
import spidev

try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("smartfarmbase-firebase-adminsdk-8vmv8-5f0892865a.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://smartfarmbase-default-rtdb.firebaseio.com/smartfarm'
        })
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

soil_ref = db.reference()

soil_get_ref = db.reference('SaveSoilMos')

Mode_ref = db.reference('Mode')
ref = db.reference('Water')
water_ref = db.reference()
FB_Change1 = db.reference('Change')

Change1 = 0
mode = 0
SM = 0

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def readChannel(channel):
    val = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((val[1]&3) << 8) + val[2]
    return data

def Percent(data):
    return int(abs(1023 - data) / 1023 * 100)

def SoilHumFB():
    while True:
        try:
            global Change1
            global mode
            Change1 = FB_Change1.get()
            if (Change1 == 1):
                SM_write = open('SoilMois.txt','w')
                SM_write.write(str(soil_get_ref.get()))
                SM_write.close()
                Change1 = 0
                
           
            
            mode = Mode_ref.get()

            if mode == 1:
                water = ref.get()
                if water == 1:
                    print('water')
                    GPIO.output(13, True)
                    sleep(3)
                    GPIO.output(13, False)
                    water_ref.update({'Water':int(0)})
                 
            val = readChannel(0)
            Soil = Percent(val)
            soil_ref.update({'SoilMos':int(Soil)})
        
        except:
            print('error')
        sleep(1)
        
def thread_run():
    global mode
    mode = 0
    threading.Timer(40, thread_run).start()

sub_work = threading.Thread(target=SoilHumFB)
sub_work.start()
thread_run()


while True:
    if (Change1 == 0):
        SM_read = open('SoilMois.txt', 'r')
        SM = SM_read.readline()
        SM_read.close()
    val = readChannel(0)
    Soil = Percent(val)
    if(mode == 0):
        if(Soil < int(SM)-20):
            GPIO.output(13, True)
            sleep(3)
            GPIO.output(13, False)
    sleep(1)