import cv2 

faceCascade= cv2.CascadeClassifier("C:/Users/rayha/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")

#img = cv2.imread("avengers.jpg")
capture = cv2.VideoCapture(1)
capture.set (3, 640)
capture.set (4, 480)
success,img = capture.read() 
while success:
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.1,20)  #Src,scaleFactor,minNeighbors

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0),2)
    cv2.imshow("Faces", img)
    
    if cv2.waitKey(16) & 0xFF==ord('x'):
        break
    if cv2.getWindowProperty("Faces", cv2.WND_PROP_VISIBLE) <1:
        break
    success, img = capture.read()

capture.release()
cv2.destroyAllWindows()