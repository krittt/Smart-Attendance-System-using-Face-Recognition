
import pymongo  
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def take_attendance(class_sub,selection):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dblist = myclient.list_database_names()
    mydb = myclient["students"]
    hindi_subject = mydb["Hindi"]
    english_subject= mydb["English"]
    path = 'images'
    images = []
    personNames = []
    myList = os.listdir(path)
    print(myList)
    for cu_dir in myList:
        current_dir=os.listdir(path+"/"+cu_dir)
        # print(current_dir)
        for cu_img in current_dir:
            current_Img = cv2.imread(f'{path}/{cu_dir}/{cu_img}')
            images.append(current_Img)
            personNames.append(cu_dir)
    print(personNames)
    # print(images)

    def faceEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    # print(faceEncodings(images))
    
    def attendance(name):
        with open(f'{class_sub}', 'r+') as f:
            i=name.find('_')
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name[0:i] not in nameList:
                time_now = datetime.now()
                tStr = time_now.strftime('%H:%M:%S')
                dStr = time_now.strftime('%d/%m/%Y')
                f.writelines(f'{name[0:i]},{name[i+1:]},{tStr},{dStr}\n')
                mydict=[{"Roll_Number":name[0:i],"Name":name[i+1:],"Time":tStr,"Date":dStr}]
                if(selection==1):
                    x = hindi_subject.insert_many(mydict)
                else:
                    y = english_subject.insert_many(mydict)



    encodeListKnown = faceEncodings(images)
    print('All Encodings Complete!!!')

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = personNames[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                attendance(name)

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()

