import cv2 

faceCascade= cv2.CascadeClassifier("C:/Users/rayha/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
img = cv2.imread("avengers.jpg")
shape = img.shape
scale = tuple(int(dim/2) for dim in shape[0:2])
img = cv2.resize(img, (scale[1],scale[0]))

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(imgGray,1.1,10)  #Src,scaleFactor,minNeighbors

for (x,y,w,h) in faces:
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0),2)
    
cv2.imshow("Face Detector",img)
cv2.waitKey(0)