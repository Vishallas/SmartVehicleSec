import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import time


path = f"{os.getcwd()}/recog/secreteKey/facerecogvehiclesecsyst-firebase-adminsdk-br0ka-d10101ff43.json"
#print(path)

class DatabaseHelper:
    cred_obj = None
    def __init__(self):
        cred_obj = credentials.Certificate(path)
        firebase_admin.initialize_app(cred_obj, {'storageBucket': 'facerecogvehiclesecsyst.appspot.com'})
        self.db = firestore.client()
        self.imgNo = int(self.db.collection('VehicleData').document("location").get().to_dict()['imgNo'])
        self.fileName = f"{os.getcwd()}/unauthorthorized/k.jpg"
        self.bucket = storage.bucket()

    def updatelocation(self,lat,long):
        print(f"Latitude - {lat}.\nLongitude - {long}.\n")
        self.db.collection('VehicleData').document("location").update({'lat':f'{lat}','long':f'{long}',"time":firestore.SERVER_TIMESTAMP})
    
    def sendImage(self):
        blob = self.bucket.blob("UnaurthoPerson"+str(self.imgNo+1))
        blob.upload_from_filename(f"{os.getcwd()}/unauthorthorized/k.jpg")
        blob.make_public()
        time.sleep(3)
        return blob.public_url

    def linkimage(self,imagelink,lat,long):
        print("link :",imagelink)
        # self.db.collection('VehicleData').document("imagedata").update({'link':f'{imagelink}'})
        self.db.collection('VehicleData').document("location").update({'lat':f'{lat}','long':f'{long}',"time":firestore.SERVER_TIMESTAMP,'image_url':f'{imagelink}'})
        self.db.collection('VehicleData').document("location").update({'image_url':f'{imagelink}'})
