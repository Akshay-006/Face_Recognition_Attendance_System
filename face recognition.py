import threading
import mysql.connector as db

from deepface import DeepFace
import cv2






cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)# idhu vandhu capturing variable cap

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,480)

counter=0
Face_match=False

ref=cv2.imread("final.jpeg") #idhaan kuduthurken , final.jpeg so adha enter panren db la
def check_face(img):
    global Face_match
    try:
        if DeepFace.verify(frame,ref.copy())['verified']:
            Face_match=True
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
        else:
            cv2.putText(frame, " NO MATCH !", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("OUT",frame)




    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyWindow()


