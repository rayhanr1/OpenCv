import cv2
import numpy as np
import imutils

capture = cv2.VideoCapture(0)
capture.set(3,3840)
capture.set(4,2160)

myColors = [[6,111,63,39,255,255]]
            #[77,86,135,93,255,255],
            #[102,73,91,112,255,255]
            

myColorValues = [[0,128,255],
                 [102,204,0],
                 [204,0,0]]

myPoints = []

def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0 
    newPoints=[]
    for color in myColors:
        lower= np.array(color[0:3])
        upper= np.array(color[3:])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
            
        count+=1  
    return newPoints
        #cv2.imshow(str(color[0]),mask)

def getContours(img):
    contours = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    x,y,w,h =0,0,0,0
    for cont in contours:
        area = cv2.contourArea(cont)
        if area>300:
            #cv2.drawContours(imgResult,cont,-1,(255,0,0),3)   
            perimeter = cv2.arcLength(cont,True)
            approx = cv2.approxPolyDP(cont, .03*perimeter, True)
            x,y,w,h = cv2.boundingRect(approx)         
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)

success, vid = capture.read()        
while success:    
    vid = cv2.flip(vid, 1)
    vid = cv2.resize(vid, (480,360)) 
    imgResult = vid.copy()
    newPoints = findColor(vid,myColors,myColorValues) 
    if len(newPoints)!=0:
        for newPoint in newPoints:
            myPoints.append(newPoint)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints, myColorValues)
            
    cv2.imshow("Video",imgResult)
    
    if cv2.waitKey(16) & 0xFF==ord('x'):
        break
    
    if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) <1:
        break
    
    success, vid = capture.read() 
capture.release()
cv2.destroyAllWindows()
