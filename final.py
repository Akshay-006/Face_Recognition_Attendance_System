import threading
import mysql.connector as db

from deepface import DeepFace

import cv2
from datetime import datetime
current_date = datetime.now().date()

employee={"Akshay R":"real.jpeg"}
conn=db.connect(
    host="localhost",
    user="root",
    database="attendence",
    password="password"
)

cursor=conn.cursor()


cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)# idhu vandhu capturing variable cap

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,480)

counter=0
Face_match=False



def check_face(img):
    global Face_match
    global img1
    for i,j in employee.items():
        ref = cv2.imread(j)  # aanaa tuple aa irukum so adha string aa mathanu mfirst
        try:
            if DeepFace.verify(frame,ref.copy())['verified']:
                img1=i
                Face_match=True
                '''cursor.execute(f"insert into employee (Name,Attendence) values ({img1},'present'")
                conn.commit()'''

            else:
                Face_match=False
        except:
            Face_match=False




while True:
    ret,frame =cap.read()

    if ret:
        if counter%30==0:
            try:
                threading.Thread(target=check_face,args=(frame.copy(),)).start()


            except ValueError:
                pass
        counter+=1

        if Face_match:
            cv2.putText(frame,"MATCH !",(20,450) ,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
            #print(img1)
            cursor.execute(f"insert ignore into employee (Name,Attendence) values ('{img1}','present') ON DUPLICATE KEY UPDATE name = '{img1}', attendence = 'present';")
            conn.commit()


        else:
            cv2.putText(frame, " NO MATCH !", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("OUT",frame)




        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


#print(emp)

conn.close()

cap.release()
cv2.destroyWindow()


