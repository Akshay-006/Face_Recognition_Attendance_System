import threading
import mysql.connector as db

from deepface import DeepFace
import cv2



employee_images=[]
emp=[]
conn=db.connect(
    host="localhost",
    user="root",
    database="face_recognition",
    password="password"
)

cursor=conn.cursor()

select_query ="Select image from employee;"

cursor.execute(select_query)

result=cursor.fetchall()

for i in result:
    employee_images.append(i)

for i in employee_images:
    str1 = ''.join(map(str, i))
    emp.append(str1)

#print(employee_images)

emp.append("real.jpeg")






cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)# idhu vandhu capturing variable cap

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,480)

counter=0
Face_match=False



def check_face(img):
    global Face_match
    global img1
    for i in emp:
        ref = cv2.imread(i)  # aanaa tuple aa irukum so adha string aa mathanu mfirst
        try:
            if DeepFace.verify(frame,ref.copy())['verified']:
                img1=i
                Face_match=True
                '''cursor.execute(f"update employee set attendence='present' where image={img1}")
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
            cursor.execute(f"update employee set attendence = 'present' where image = {img1}")
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


