import cv2
import face_recognition
import pickle
import os


imagedir = f'{os.getcwd()}\\images'
encodpath = f'{os.getcwd()}\\encodes'

#print(imagedir,encodpath)

imgspath = os.listdir(imagedir)
imgspath.remove(".gitkeep")
#print(imgspath)

def processImgs():
    imgs = []
    encodings = []
    names = []
    for imgpath in imgspath:
        curbgrimg = cv2.imread(f'{imagedir}\\{imgpath}')
        curimg = cv2.cvtColor(curbgrimg,cv2.COLOR_BGR2RGB)
        imgs.append(curimg)
        curname = os.path.splitext(imgpath)[0]
        names.append(curname)
        
    for img,name in zip(imgs,names):
        print(f'Processing image {name} ...')
        curencods = face_recognition.face_encodings(img)[0]
        encodings.append(curencods)
    return encodings,names

with open(f'{encodpath}\\encode.pickle','wb') as f1 , open(f'{encodpath}\\name.pickle','wb') as f2:
    en,nam = processImgs()
    pickle.dump(en,f1)
    pickle.dump(nam,f2)