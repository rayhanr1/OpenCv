import cv2
import numpy as np
import math
import imutils

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    contours = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    for cont in contours:
        area = cv2.contourArea(cont)
        cv2.drawContours(imgContour,cont,-1,(0,255,0),1)   
        perimeter = cv2.arcLength(cont,True)
        
        approx = cv2.approxPolyDP(cont, .03*perimeter, True)
        print(len(approx))
        
        objCorner = len(approx)
        x,y,w,h = cv2.boundingRect(approx)
        ar = w/float(h)
        
        if objCorner ==3:
            objType = "Triangle"
        elif objCorner ==4:
            if .95<ar<1.05:
                objType = "Square"
            else:
                objType = "Rectangle"
        elif objCorner==5:
            objType = "Pentagon"
            
        elif objCorner==6:
            objType="Hexagon"
            
        elif objCorner==8 and .95<ar<1.05:
            objType="Octagon"
        
        else:
            objType="Other"
        
        
        value=str(math.sqrt(area)/perimeter)
        print(value)
        cv2.putText(imgContour, objType, (x+(w//2)-10,y+(h//2)-10), cv2.FONT_HERSHEY_COMPLEX,.5,(0,0,0),2)
        cv2.rectangle(imgContour,(x,y),(x+w,y+h),(255,0,0),3)
        


img = cv2.imread("shapes.png")
shape = img.shape
scale = tuple(int(dim/2) for dim in shape[0:2])
img = cv2.resize(img, (scale[1],scale[0]))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
imgCanny = cv2.Canny(imgBlur,50,50)
imgBlank = np.zeros_like(img)
imgContour = img.copy()
getContours(imgCanny)

imgStack = stackImages(.6,([img,imgGray,imgBlur],
                           [imgCanny,imgContour,imgBlank]))
stackShape = imgStack.shape
stackScale = tuple(int(dim/1.2) for dim in stackShape[0:2])
imgStack = cv2.resize(imgStack, (stackScale[1],stackScale[0]))

cv2.imshow("Stack",imgStack)
cv2.waitKey(0)