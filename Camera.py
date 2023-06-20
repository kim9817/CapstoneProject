print('Camera.py-execute')

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


from picamera import PiCamera
from time import sleep
import sys, os
import requests
from uuid import uuid4

PROJECT_ID = "smartfarmbase"


try:
    app = firebase_admin.get_app()
except:
    cred = credentials.Certificate("smartfarmbase-firebase-adminsdk-8vmv8-5f0892865a.json")
    default_app = firebase_admin.initialize_app(cred, {
    'storageBucket' : f"{PROJECT_ID}.appspot.com"})

bucket = storage.bucket()

def fileUpload(file):
    blob = bucket.blob(file)
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token}
    blob.metadata = metadata
    blob.upload_from_filename(filename = '/home/pi/'+file, content_type = 'image/jpg')
    
    


camera = PiCamera()
camera.resolution = (350, 216)

while True:
    try:
        camera.capture('/home/pi/image.jpg')
        fileUpload('image.jpg')
        sleep(1)
    except:
        print('error')