# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 20:58:36 2022

@author: Athul
"""

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
path = 'FINAL DATABASE'
images =[]
Names =[]
myList = os.listdir(path)
for cls in myList:
 cur_img = cv2.imread(f'{path}/{cls}')
 images.append(cur_img)
 Names.append(os.path.splitext(cls)[0])
def GetEncodings(images):
 encodelist =[]
 for img in images:
 img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 encoding = face_recognition.face_encodings(img)[0]
 encodelist.append(encoding)
 return encodelist
def markatd(name):
 with open('Attendance List.csv', 'r+') as f:
 datalist = f.readlines()
 namelist =[]
 for line in datalist:
 entry = line.split(',')
 namelist.append(entry[0])
 if name not in namelist:
 now = datetime.now()
 date=now.strftime('%d-%m-%Y')
 time = now.strftime('%H:%M:%S')
 status='Present'
 f.writelines(f'\n{name},{date},{time},{status}')
encodeknownlist = GetEncodings(images)
print('Encoding Completed!!')
cam = cv2.VideoCapture(0)
while True:
 success, img = cam.read()
 small_img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
 small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)
 facecurframe = face_recognition.face_locations(small_img)
 encodecurframe = face_recognition.face_encodings(small_img, facecurframe)
 for encodeface, faceloc in zip(encodecurframe, facecurframe):
 matches = face_recognition.compare_faces(encodeknownlist, encodeface)
 face_dist = face_recognition.face_distance(encodeknownlist, encodeface)
 matchindex = np.argmin(face_dist)
 if face_dist[matchindex] < 0.60:
 name = Names[matchindex].upper()
 markatd(name)
 else:
 name = 'Unknown'
 y1, x2, y2, x1 = faceloc
 y1 = y1 * 4
 x2 = x2 * 4
 y2 = y2 * 4
 x1 = x1 * 4
 cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
 cv2.rectangle(img, (x1, y2 - 35), (x2+120, y2+40), (255, 0, 255),
cv2.FILLED)
 cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX,
1, (255, 255, 255), 2)
 if(name!='Unknown'):
 cv2.putText(img, 'Status:Present', (x1, y2 + 36),
cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
 cv2.imshow('Webcam', img)
 cv2.waitKey(1)