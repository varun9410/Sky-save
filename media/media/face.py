import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle
import requests
import easygui

msg = "Hello !!!\n Welcome to Attendance Software"
title = "LiveAttendance"
choices = ["Enable Attendance"]


path = 'office-team'
images = []
classNames = []
mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList
encoded_face_train = findEncodings(images)

def markAttendanceEntry(name, frame, img_counter):
    API_ENDPOINT = "https://api.walkinmart.in/api/add_tbl_attendance?branch_id=ND110"
    with open('AttendanceEntry.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'\n{name}, {time}, {date}')
            data = {'store_id' : '4',
                    'emp_id' : name,
                    'type':'IN'}
            #r = requests.post(url = API_ENDPOINT, data = data)
            print(name)
            #Taking snapshot
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))

def markAttendanceExit(name, frame, img_counter):
    API_ENDPOINT = "https://api.walkinmart.in/api/add_tbl_attendance?branch_id=ND110"
    with open('AttendanceEntry.csv','r+') as f: 
        with open('AttendanceExit.csv','r+') as g:
            myDataList = f.readlines()
            nameList = []
            exit = []
            myExitData = g.readlines()
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            for line in myExitData:
                entry = line.split(',')
                exit.append(entry[0])
            if (name in nameList) and (name not in exit):
                now = datetime.now()
                time = now.strftime('%I:%M:%S:%p')
                date = now.strftime('%d-%B-%Y')
                g.writelines(f'\n{name}, {time}, {date}')
                data = {'store_id' : '4',
                        'emp_id' : name,
                        'type':'OUT'}
                #r = requests.post(url = API_ENDPOINT, data = data)
                print(name)
                #Taking snapshot
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))

def capture():
   # cap  = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('rtsp://admin:admin123@192.168.1.73:554/cam/realmonitor?channel=1&subtype=0')
    img_counter = 0
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
        for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
            matches = face_recognition.compare_faces(encoded_face_train, encode_face)
            faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
            matchIndex = np.argmin(faceDist)
            print(matchIndex)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper().lower()
                y1,x2,y2,x1 = faceloc
                # since we scaled down by 4 times
                y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
                cv2.putText(img,name, (x1+6,y2-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendanceExit(name, img, img_counter)
                print(name)
                img_counter += 1
        cv2.imshow('webcam2', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

reply = easygui.buttonbox(msg, title, choices = choices)
if reply == "Enable Attendance":
    capture()
