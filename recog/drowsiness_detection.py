#Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
#face_utils for basic operations of conversion
from imutils import face_utils
#import serial
import time
import os

from webcamvideostream import WebcamVideoStream

class drowsiness:
    def __init__(self,v1):
        #self.s = serial.Serial('COM5',9600)
        #Initializing the camera and taking the instance
        # cap = cv2.VideoCapture(0)
        #Initializing the face detector and landmark detector
        self.hog_face_detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(f"{os.getcwd()}/recog/shape_predictor_68_face_landmarks.dat")
        #status marking for current state
        self.sleep = 0
        self.drowsy = 0
        self.active=0
        self.status="------------"
        self.color = (0,0,255)
        self.v1 = v1

    def compute(self,ptA,ptB):
        dist = np.linalg.norm(ptA - ptB)
        return dist
    def blinked(self,a,b,c,d,e,f):
        up = self.compute(b,d) + self.compute(c,e)
        down = self.compute(a,f)
        ratio = up/(2.0*down)

        #Checking if it is blinked
        if(ratio>0.25):
            return 2
        elif(ratio>0.21 and ratio<=0.25):
            return 1
        else:
            return 0
    def drowssy(self):
        t = time.time()
        
        while True:
            z=int(time.time())-int(t)
            frame = self.v1.read()
            #_,frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.putText(frame,"Drowsiness Detection",(130,40),cv2.FONT_HERSHEY_PLAIN,2,(255, 0, 63),2)
            faces = self.hog_face_detector(gray)
            #detected face in faces array
            for face in faces:
                    x1 = face.left()
                    y1 = face.top()
                    x2 = face.right()
                    y2 = face.bottom()
                    face_frame = frame.copy()
                    cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    landmarks = self.predictor(gray, face)
                    landmarks = face_utils.shape_to_np(landmarks)
                    #The numbers are actually the landmarks which will show eye
                    left_blink = self.blinked(landmarks[36],landmarks[37], 
                    landmarks[38], landmarks[41], landmarks[40], landmarks[39])
                    right_blink = self.blinked(landmarks[42],landmarks[43], 
                    landmarks[44], landmarks[47], landmarks[46], landmarks[45])

                    #Now judge what to do for the eye blinks
                    if(left_blink==0 or right_blink==0):
                        self.sleep+=z
                        if(z>3):
                            self.status = "SLEEPING !!!"
                            t=time.time()
                        # if(self.sleep>6):
                        #     #s.write(b'a')
                        #     # time.sleep(0.5)
                        #     self.status="SLEEPING !!!"
                        self.drowsy=0
                        self.active=0

                    elif(left_blink==1 or right_blink==1):
                        self.drowsy+=z
                        if(self.drowsy>6):
                            # s.write(b'a')
                            # time.sleep(0.5)
                            self.status="Drowsy !"
                            t=time.time()
                        self.sleep=0
                        self.active=0

                    else:
                        self.active+=z
                        if(self.active>6 and self.drowsy<6):
                            # s.write(b'b')
                            # time.sleep(0.5)
                            self.status="Active :)"
                            t=time.time()
                        self.drowsy=0
                        self.sleep=0

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                    cv2.putText(frame, self.status, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.color,3)
                    for n in range(0, 68):
                        (x,y) = landmarks[n]
                        cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)
            
            
            cv2.imshow("Frame", frame)
            #cv2.imshow("Result of detector", face_frame)
            key = cv2.waitKey(1)
            if key == 27:
                    break
