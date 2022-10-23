import cv2
from functools import wraps
from pygame import mixer
import time
x = 0
def counter(func):
    @wraps(func)
    def tmp(*args, **secondargs):
        tmp.count += 1
        global x
        if time.time() - x > 1:
            x = time.time()
            tmp.count = 0
        return func(*args, **secondargs)
    tmp.count = 0
    return tmp
face_cascade = cv2.CascadeClassifier('frontface.xml')
eye_cascade = cv2.CascadeClassifier('eyes.xml')
cap = cv2.VideoCapture(0)
@counter
def sound():
    mixer.init()
    mixer.music.load('alarm.mp3')
    mixer.music.play()
def eyeisclosed():
    print ("The Driver eyes are currently closed and is sleeping")
def openeye():
    print("The Driver eyes are currently open and is driving with full attention!!")
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # region of intrest-selecting height of colours
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if eyes is not ():
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                openeye()
        else:
            eyeisclosed()
            if eyeisclosed.count == 1:
                print ("Driver is not alert and sleeping currently!!")
                sound()
    cv2.imshow('img', img)
    k = cv2.waitKey(1) & 0xff
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()